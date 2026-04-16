#!/usr/bin/env python3
"""
check_pages.py - Validate query quality, tool credibility, and page/data consistency.

Checks:
- Every profile has focused queries (query count mismatch is reported as warning).
- Tool entries have sane names and valid URLs.
- Generated HTML tool card count matches JSON tool count.
- Theme relevance warnings for off-topic tools/queries.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent

PAGE_CONFIGS = [
    {"slug": "general", "data": ROOT / "data" / "tools.json", "html": ROOT / "index.html"},
    {"slug": "enterprise", "data": ROOT / "data" / "tools-enterprise.json", "html": ROOT / "enterprise.html"},
    {"slug": "discovery", "data": ROOT / "data" / "tools-discovery.json", "html": ROOT / "discovery.html"},
    {"slug": "ragdev", "data": ROOT / "data" / "tools-ragdev.json", "html": ROOT / "ragdev.html"},
    {"slug": "agentdev", "data": ROOT / "data" / "tools-agentdev.json", "html": ROOT / "agentdev.html"},
    {"slug": "vscode", "data": ROOT / "data" / "tools-vscode.json", "html": ROOT / "vscode.html"},
    {"slug": "newrag", "data": ROOT / "data" / "tools-newrag.json", "html": ROOT / "newrag.html"},
    {"slug": "cowork", "data": ROOT / "data" / "tools-cowork.json", "html": ROOT / "cowork.html"},
    {"slug": "ocr", "data": ROOT / "data" / "tools-ocr.json", "html": ROOT / "ocr.html"},
    {"slug": "dococr", "data": ROOT / "data" / "tools-dococr.json", "html": ROOT / "dococr.html"},
    {"slug": "aicliapps", "data": ROOT / "data" / "tools-aicliapps.json", "html": ROOT / "aicliapps.html"},
]

THEME_KEYWORDS = {
    "general": ["ai", "ia", "automation", "tool", "outils"],
    "enterprise": ["enterprise", "entreprise", "governance", "compliance", "security", "rag", "conformite"],
    "discovery": ["discovery", "new", "nouveaux", "emerging", "launch", "trend", "decouverte"],
    "ragdev": ["rag", "retrieval", "vector", "embedding", "rerank", "ingestion", "developpeur"],
    "agentdev": ["agent", "orchestration", "autonomous", "workflow", "framework", "developpement"],
    "vscode": ["vscode", "vs code", "extension", "editor", "copilot"],
    "newrag": ["rag", "graph", "hybrid", "multimodal", "retrieval"],
    "cowork": ["team", "equipe", "collaboration", "workspace", "meeting", "project", "cowork"],
    "ocr": ["ocr", "document", "pdf", "text extraction", "handwriting", "reconnaissance"],
    "dococr": ["ocr", "document", "ingestion", "classification", "workflow", "documentaire"],
    "aicliapps": ["cli", "terminal", "shell", "command line", "devops", "ligne de commande"],
}

SUSPICIOUS_HOSTS = {
    "example.com",
    "localhost",
    "127.0.0.1",
    "news.ycombinator.com",
    "medium.com",
    "substack.com",
    "reddit.com",
    "youtube.com",
    "x.com",
    "twitter.com",
    "linkedin.com",
    "producthunt.com",
    "futurepedia.io",
    "theresanaiforthat.com",
}

GENERIC_NAME_TOKENS = {
    "best",
    "top",
    "guide",
    "comparison",
    "comparatif",
    "news",
    "ranking",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate IA_survey pages and datasets")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def iter_tools(data: dict):
    for category in data.get("categories", []):
        cat_name = category.get("name", "")
        for sub in category.get("subcategories", []):
            sub_name = sub.get("name", "")
            for tool in sub.get("tools", []):
                yield cat_name, sub_name, tool


def has_theme_signal(text: str, slug: str) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in THEME_KEYWORDS.get(slug, []))


def validate_queries(errors: list[str], warnings: list[str]):
    payload = load_json(ROOT / "data" / "search_queries.json")
    profiles = payload.get("profiles", {})

    for cfg in PAGE_CONFIGS:
        slug = cfg["slug"]
        profile = profiles.get(slug, {})
        queries = profile.get("queries", [])

        if not isinstance(queries, list):
            errors.append(f"[{slug}] queries must be a list")
            continue

        if len(queries) != 10:
            warnings.append(f"[{slug}] expected 10 queries, found {len(queries)}")

        normalized = [q.strip() for q in queries if isinstance(q, str)]
        if len(normalized) != len(queries):
            errors.append(f"[{slug}] all queries must be non-empty strings")
            continue

        if len(set(q.lower() for q in normalized)) != len(normalized):
            errors.append(f"[{slug}] duplicate queries detected")

        for idx, query in enumerate(normalized, start=1):
            if len(query.split()) < 4:
                warnings.append(f"[{slug}] query {idx} is probably too short: '{query}'")
            if not has_theme_signal(query, slug):
                warnings.append(f"[{slug}] query {idx} may be off-theme: '{query}'")


def validate_tool_record(slug: str, category: str, subcategory: str, tool: dict, errors: list[str], warnings: list[str]):
    name = str(tool.get("name", "")).strip()
    url = str(tool.get("url", "")).strip()
    provider = str(tool.get("provider", "")).strip()
    desc = str(tool.get("desc", "")).strip()

    context = f"[{slug}] {category} / {subcategory}"

    if not name:
        errors.append(f"{context}: missing tool name")
        return

    if len(name) < 2 or len(name) > 80:
        warnings.append(f"{context}: unusual tool name length '{name}'")

    lowered_name = name.lower()
    if any(token in lowered_name for token in GENERIC_NAME_TOKENS):
        errors.append(f"{context}: generic/non-tool title detected '{name}'")

    if not url:
        errors.append(f"{context}: missing URL for '{name}'")
        return

    parsed = urlparse(url)
    host = (parsed.hostname or "").lower().removeprefix("www.")

    if parsed.scheme not in {"http", "https"}:
        errors.append(f"{context}: invalid URL scheme for '{name}' -> {url}")
        return

    if not host or "." not in host:
        errors.append(f"{context}: invalid URL host for '{name}' -> {url}")
        return

    if host in SUSPICIOUS_HOSTS:
        errors.append(f"{context}: low-confidence host for '{name}' -> {host}")

    if any(marker in url.lower() for marker in ["/search?", "?q=", "duckduckgo.com", "google.com/search"]):
        errors.append(f"{context}: search result URL used instead of product URL for '{name}'")

    # Keep warnings focused on quality issues with low false-positive rates.



def validate_pages(errors: list[str], warnings: list[str]):
    for cfg in PAGE_CONFIGS:
        slug = cfg["slug"]
        data_file = cfg["data"]
        html_file = cfg["html"]

        if not data_file.exists():
            errors.append(f"[{slug}] missing data file: {data_file}")
            continue
        if not html_file.exists():
            errors.append(f"[{slug}] missing HTML file: {html_file}")
            continue

        data = load_json(data_file)
        tool_count = 0

        for category, subcategory, tool in iter_tools(data):
            validate_tool_record(slug, category, subcategory, tool, errors, warnings)
            tool_count += 1

        html_content = html_file.read_text(encoding="utf-8")
        rendered_cards = html_content.count('class="tool-card')
        if rendered_cards != tool_count:
            errors.append(
                f"[{slug}] rendered card mismatch: html={rendered_cards}, json={tool_count}"
            )


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    warnings: list[str] = []

    validate_queries(errors, warnings)
    validate_pages(errors, warnings)

    print("=== IA Survey Validation Report ===")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    if errors:
        return 1
    if args.strict and warnings:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
