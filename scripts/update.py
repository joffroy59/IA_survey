#!/usr/bin/env python3
"""
update.py — Recherche de nouveaux outils IA et mise à jour de tools.json
APIs gratuites : DuckDuckGo (search) + Google Gemini Flash (LLM)
"""

import json
import os
import sys
import time
import argparse
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

# ── Trace module (local) ──────────────────────────────────────────────────────
from trace import get_tracer, initialize_tracer

# ── Dépendances ──────────────────────────────────────────────────────────────
try:
    from ddgs import DDGS
    import google.generativeai as genai
    from google.api_core import exceptions as google_api_exceptions
except ImportError:
    print("Installing dependencies...")
    os.system("pip install ddgs google-generativeai --quiet")
    from ddgs import DDGS
    import google.generativeai as genai
    from google.api_core import exceptions as google_api_exceptions

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SEARCH_QUERIES_FILE = ROOT / "data" / "search_queries.json"

PROFILE_CONFIG = {
    "general": {
        "tools_file": ROOT / "data" / "tools.json",
        "page_name": "general",
        "page_label": "Panorama Generaliste",
        "page_description": "Vue complete des meilleurs outils IA grand public et pro.",
        "query_profile": "general",
    },
    "enterprise": {
        "tools_file": ROOT / "data" / "tools-enterprise.json",
        "page_name": "enterprise",
        "page_label": "Panorama Enterprise",
        "page_description": "Focus RAG, agents, infra, securite et cas d'usage entreprise.",
        "query_profile": "enterprise",
    },
    "discovery": {
        "tools_file": ROOT / "data" / "tools-discovery.json",
        "page_name": "discovery",
        "page_label": "Panorama Decouverte",
        "page_description": "Version optimisee des requetes generales pour detecter les nouveautes.",
        "query_profile": "discovery",
    },
    "ragdev": {
        "tools_file": ROOT / "data" / "tools-ragdev.json",
        "page_name": "ragdev",
        "page_label": "Panorama RAG Pro + DevTools",
        "page_description": "Focus architecture RAG production et outils IA pour developpeurs.",
        "query_profile": "ragdev",
    },
    "agentdev": {
        "tools_file": ROOT / "data" / "tools-agentdev.json",
        "page_name": "agentdev",
        "page_label": "Panorama Agent Dev + IDE Tools",
        "page_description": "Outils spécialisés pour développement d'agents IA autonomes et IDE enrichis d'IA.",
        "query_profile": "agentdev",
    },
    "vscode": {
        "tools_file": ROOT / "data" / "tools-vscode.json",
        "page_name": "vscode",
        "page_label": "Panorama VS Code + Extensions IA",
        "page_description": "Outils, extensions et workflows IA dédiés à VS Code.",
        "query_profile": "vscode",
    },
    "newrag": {
        "tools_file": ROOT / "data" / "tools-newrag.json",
        "page_name": "newrag",
        "page_label": "Panorama New RAG",
        "page_description": "Nouveaux frameworks, patterns et plateformes RAG 2026.",
        "query_profile": "newrag",
    },
    "cowork": {
        "tools_file": ROOT / "data" / "tools-cowork.json",
        "page_name": "cowork",
        "page_label": "Panorama Cowork IA",
        "page_description": "Collaboration assistée par IA pour équipes produit, dev et ops.",
        "query_profile": "cowork",
    },
    "ocr": {
        "tools_file": ROOT / "data" / "tools-ocr.json",
        "page_name": "ocr",
        "page_label": "Panorama OCR",
        "page_description": "Outils OCR, extraction de texte et traitement intelligent de documents.",
        "query_profile": "ocr",
    },
    "dococr": {
        "tools_file": ROOT / "data" / "tools-dococr.json",
        "page_name": "dococr",
        "page_label": "Panorama Système OCR Complet",
        "page_description": "Plateformes complètes pour ingestion, OCR, classification et workflow documentaire.",
        "query_profile": "dococr",
    },
    "aicliapps": {
        "tools_file": ROOT / "data" / "tools-aicliapps.json",
        "page_name": "aicliapps",
        "page_label": "Panorama AI CLI Applications",
        "page_description": "Applications IA en ligne de commande pour developpeurs, DevOps et automatisation.",
        "query_profile": "aicliapps",
    },
}

MAX_SEARCH_RESULTS = 15  # par requête
GEMINI_RETRY_WAIT_SECONDS = 60
MAX_SEARCH_CONTEXT_LINES = 80

# Ordered list of Gemini models to try. On quota exhaustion the next model is used.
GEMINI_MODELS = [
    "gemini-2.5-pro",
    "gemini-2.5-flash",
]

AICLIAPPS_CATEGORIES = [
    {
        "id": "cli_agents",
        "name": "Agents et assistants CLI",
        "icon": "🤖",
        "subcategories": [
            {"name": "Assistants terminal", "icon": "💻", "tools": []},
            {"name": "Agents autonomes CLI", "icon": "🧭", "tools": []},
        ],
    },
    {
        "id": "cli_dev",
        "name": "Dev et code en CLI",
        "icon": "🛠️",
        "subcategories": [
            {"name": "Code generation et refactor", "icon": "🧩", "tools": []},
            {"name": "Qualite et tests", "icon": "✅", "tools": []},
        ],
    },
    {
        "id": "cli_ops",
        "name": "DevOps et automatisation",
        "icon": "⚙️",
        "subcategories": [
            {"name": "Infra et pipeline", "icon": "🏗️", "tools": []},
            {"name": "Automatisation shell", "icon": "📟", "tools": []},
        ],
    },
    {
        "id": "cli_local",
        "name": "Local LLM et self-hosted",
        "icon": "🖥️",
        "subcategories": [
            {"name": "Inference locale", "icon": "📦", "tools": []},
            {"name": "Tooling self-hosted", "icon": "🔒", "tools": []},
        ],
    },
    {
        "id": "cli_security",
        "name": "Securite et gouvernance",
        "icon": "🛡️",
        "subcategories": [
            {"name": "Conformite entreprise", "icon": "🏢", "tools": []},
            {"name": "Controle des acces", "icon": "🔐", "tools": []},
        ],
    },
]

AICLIAPPS_KEYWORD_RULES = [
    ("cli_security", "Conformite entreprise", ["security", "securite", "compliance", "conformite", "governance", "gouvernance", "gdpr", "audit"]),
    ("cli_local", "Inference locale", ["local", "self-hosted", "self hosted", "ollama", "llama.cpp", "inference", "gpu", "offline"]),
    ("cli_ops", "Infra et pipeline", ["devops", "sre", "ci/cd", "pipeline", "terraform", "kubernetes", "docker", "deployment"]),
    ("cli_ops", "Automatisation shell", ["bash", "shell", "terminal", "automation", "automatisation", "script", "command line", "cli"]),
    ("cli_dev", "Qualite et tests", ["test", "lint", "quality", "qualite", "review", "debug", "profiling"]),
    ("cli_dev", "Code generation et refactor", ["code", "coding", "developer", "developpeur", "refactor", "pair programming"]),
    ("cli_agents", "Agents autonomes CLI", ["agent", "agentic", "autonomous", "autonome"]),
    ("cli_agents", "Assistants terminal", ["assistant", "copilot", "terminal assistant"]),
]

EXCLUDED_SEARCH_HOSTS = {
    "news.ycombinator.com",
    "medium.com",
    "substack.com",
    "reddit.com",
    "youtube.com",
    "x.com",
    "twitter.com",
    "linkedin.com",
    "futurepedia.io",
    "theresanaiforthat.com",
    "producthunt.com",
}

DISALLOWED_TOOL_HOSTS = EXCLUDED_SEARCH_HOSTS | {
    "example.com",
    "localhost",
    "127.0.0.1",
}

GENERIC_TOOL_NAME_TOKENS = {
    "best",
    "top",
    "guide",
    "comparison",
    "comparatif",
    "news",
    "ranking",
}

KNOWN_CLI_TOOL_CATALOG = [
    {
        "name": "Claude Code",
        "provider": "Anthropic",
        "url": "https://www.anthropic.com/claude-code",
        "keywords": ["claude code", "anthropic cli"],
        "category_id": "cli_dev",
        "subcategory_name": "Code generation et refactor",
    },
    {
        "name": "Aider",
        "provider": "Aider",
        "url": "https://aider.chat/",
        "keywords": ["aider", "aider chat"],
        "category_id": "cli_dev",
        "subcategory_name": "Code generation et refactor",
    },
    {
        "name": "Open Interpreter",
        "provider": "OpenInterpreter",
        "url": "https://github.com/OpenInterpreter/open-interpreter",
        "keywords": ["open interpreter", "open-interpreter"],
        "category_id": "cli_agents",
        "subcategory_name": "Agents autonomes CLI",
    },
    {
        "name": "ShellGPT",
        "provider": "ShellGPT",
        "url": "https://github.com/TheR1D/shell_gpt",
        "keywords": ["shellgpt", "shell gpt", "sgpt"],
        "category_id": "cli_agents",
        "subcategory_name": "Assistants terminal",
    },
    {
        "name": "Ollama",
        "provider": "Ollama",
        "url": "https://ollama.com/",
        "keywords": ["ollama"],
        "category_id": "cli_local",
        "subcategory_name": "Inference locale",
    },
    {
        "name": "llama.cpp",
        "provider": "llama.cpp",
        "url": "https://github.com/ggerganov/llama.cpp",
        "keywords": ["llama.cpp", "llama cpp"],
        "category_id": "cli_local",
        "subcategory_name": "Inference locale",
    },
    {
        "name": "Fabric",
        "provider": "Fabric",
        "url": "https://github.com/danielmiessler/fabric",
        "keywords": ["fabric ai", "danielmiessler/fabric"],
        "category_id": "cli_ops",
        "subcategory_name": "Automatisation shell",
    },
    {
        "name": "Warp",
        "provider": "Warp",
        "url": "https://www.warp.dev/",
        "keywords": ["warp terminal", "warp ai"],
        "category_id": "cli_agents",
        "subcategory_name": "Assistants terminal",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update AI tools datasets")
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILE_CONFIG.keys()),
        default="general",
        help="Dataset profile to update",
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="Enable verbose trace mode (logs all operations)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry-run mode: trace operations without executing AI calls or writing files",
    )
    parser.add_argument(
        "--trace-output",
        type=Path,
        default=None,
        help="Save trace log to JSON file (e.g., trace_output.json)",
    )
    return parser.parse_args()


def load_search_queries() -> dict[str, list[str]]:
    if not SEARCH_QUERIES_FILE.exists():
        raise FileNotFoundError(f"Missing search query note file: {SEARCH_QUERIES_FILE}")

    with open(SEARCH_QUERIES_FILE, "r", encoding="utf-8") as f:
        payload = json.load(f)

    profiles = payload.get("profiles", {})
    query_map: dict[str, list[str]] = {}
    for profile_name in PROFILE_CONFIG.keys():
        profile_queries = profiles.get(profile_name, {}).get("queries", [])
        if not isinstance(profile_queries, list) or not profile_queries:
            raise ValueError(f"No queries configured for profile '{profile_name}'")

        cleaned = [q.strip() for q in profile_queries if isinstance(q, str) and q.strip()]
        if len(cleaned) < 10:
            raise ValueError(
                f"Profile '{profile_name}' must define at least 10 queries, found {len(cleaned)}"
            )
        if len(set(q.lower() for q in cleaned)) != len(cleaned):
            raise ValueError(f"Profile '{profile_name}' contains duplicate queries")

        query_map[profile_name] = cleaned

    return query_map


def build_aicliapps_dataset(search_queries: list[str]) -> dict:
    return {
        "meta": {
            "title": "Boîte à outils IA Génératives",
            "subtitle": "Applications IA CLI, mis à jour automatiquement",
            "last_updated": date.today().isoformat(),
            "page_history": [],
            "page_name": "aicliapps",
            "page_label": "Panorama AI CLI Applications",
            "page_description": "Applications IA en ligne de commande pour developpeurs, DevOps et automatisation.",
            "search_queries": search_queries,
        },
        "categories": json.loads(json.dumps(AICLIAPPS_CATEGORIES)),
    }


def get_category_map(data: dict) -> dict[str, dict]:
    mapping: dict[str, dict] = {}
    for cat in data.get("categories", []):
        mapping[cat.get("id", "")] = {
            "category": cat,
            "sub_names": {sub.get("name", "").lower() for sub in cat.get("subcategories", [])},
        }
    return mapping


def infer_aicliapps_category(text: str) -> tuple[str, str]:
    lowered = text.lower()
    for cat_id, sub_name, keywords in AICLIAPPS_KEYWORD_RULES:
        if any(keyword in lowered for keyword in keywords):
            return cat_id, sub_name
    return "cli_agents", "Assistants terminal"


def resolve_category_and_subcategory(data: dict, tool: dict, profile: str) -> tuple[dict, str]:
    category_map = get_category_map(data)
    requested_cat_id = (tool.get("category_id") or "").strip()
    requested_sub_name = (tool.get("subcategory_name") or "").strip()

    if requested_cat_id in category_map:
        cat_info = category_map[requested_cat_id]
        if requested_sub_name and requested_sub_name.lower() in cat_info["sub_names"]:
            return cat_info["category"], requested_sub_name

    if profile == "aicliapps":
        source_text = " ".join(
            part for part in [tool.get("name", ""), tool.get("desc", ""), tool.get("source_text", "")] if part
        )
        inferred_cat_id, inferred_sub_name = infer_aicliapps_category(source_text)
        cat_info = category_map.get(inferred_cat_id)
        if cat_info and inferred_sub_name.lower() in cat_info["sub_names"]:
            return cat_info["category"], inferred_sub_name

    if category_map:
        first_cat = next(iter(category_map.values()))["category"]
        first_sub = first_cat.get("subcategories", [{}])[0].get("name", "Nouveaux outils")
        return first_cat, first_sub

    data.setdefault("categories", []).append({"id": "misc", "name": "Autres", "icon": "", "subcategories": []})
    return data["categories"][0], "Nouveaux outils"


def ensure_tools_file(profile: str, search_queries: list[str]):
    cfg = PROFILE_CONFIG[profile]
    tools_file = cfg["tools_file"]
    if tools_file.exists():
        return

    if profile == "aicliapps":
        with open(tools_file, "w", encoding="utf-8") as f:
            json.dump(build_aicliapps_dataset(search_queries), f, ensure_ascii=False, indent=2)
        print(f"Created missing dataset: {tools_file}")
        return

    base_file = PROFILE_CONFIG["general"]["tools_file"]
    if base_file.exists():
        with open(base_file, "r", encoding="utf-8") as f:
            base_data = json.load(f)
    else:
        base_data = {"meta": {}, "categories": []}

    base_data.setdefault("meta", {})
    base_data["meta"]["page_name"] = cfg["page_name"]
    base_data["meta"]["page_label"] = cfg["page_label"]
    base_data["meta"]["page_description"] = cfg["page_description"]
    base_data["meta"]["search_queries"] = search_queries

    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump(base_data, f, ensure_ascii=False, indent=2)
    print(f"Created missing dataset: {tools_file}")


def load_tools(tools_file: Path) -> dict:
    with open(tools_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tools(data: dict, profile: str, tools_file: Path, search_queries: list[str]):
    cfg = PROFILE_CONFIG[profile]
    data["meta"]["last_updated"] = date.today().isoformat()
    data["meta"]["page_name"] = cfg["page_name"]
    data["meta"]["page_label"] = cfg["page_label"]
    data["meta"]["page_description"] = cfg["page_description"]
    data["meta"]["search_queries"] = search_queries
    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"{tools_file.name} saved ({date.today()})")


def get_existing_names(data: dict) -> list[str]:
    names = []
    for cat in data["categories"]:
        for sub in cat.get("subcategories", []):
            for tool in sub.get("tools", []):
                names.append(tool["name"].lower())
    return names


def search_new_tools(search_queries: list[str]) -> list[dict]:
    """DuckDuckGo search — no API key required."""
    tracer = get_tracer()
    results: list[dict] = []
    with DDGS() as ddgs:
        for query in search_queries:
            try:
                response = ddgs.text(query, max_results=MAX_SEARCH_RESULTS)
                print(f"Search for '{query}'")
                hits = list(response)
                for h in hits:
                    results.append({
                        "query": query,
                        "title": h.get("title", "").strip(),
                        "body": h.get("body", "").strip(),
                        "url": h.get("href", "").strip(),
                    })
                tracer.trace_search_query(query, len(hits), results[-len(hits):] if hits else [])
                time.sleep(1)  # rate limit courtesy
            except Exception as e:
                print(f"Search error for '{query}': {e}")
                tracer.log("ERROR", "SEARCH", f"Search failed: {e}", {"query": query})
    return results[:MAX_SEARCH_CONTEXT_LINES]


def format_search_results_for_llm(search_results: list[dict]) -> str:
    lines = []
    for hit in search_results:
        lines.append(f"- [{hit.get('query', '')}] {hit.get('title', '')}: {hit.get('body', '')} ({hit.get('url', '')})")
    return "\n".join(lines)


def normalize_tool_name(raw: str) -> str:
    name = raw.strip()
    name = re.sub(r"\s+", " ", name)
    return name[:80]


def extract_name_from_title(title: str) -> str:
    if not title:
        return ""
    candidate = title
    for separator in [" - ", " | ", " – ", ": "]:
        if separator in candidate:
            candidate = candidate.split(separator)[0]
            break
    candidate = re.sub(r"\(.*?\)", "", candidate)
    candidate = re.sub(r"\[.*?\]", "", candidate)
    return normalize_tool_name(candidate)


def is_excluded_host(url: str) -> bool:
    try:
        hostname = urlparse(url).hostname or ""
    except ValueError:
        return True
    hostname = hostname.lower().removeprefix("www.")
    return hostname in EXCLUDED_SEARCH_HOSTS


def is_likely_tool_name(name: str) -> bool:
    lowered = name.lower()
    if len(name) < 3:
        return False
    if len(name) > 45:
        return False
    if any(token in lowered for token in ["best", "top", "guide", "comparatif", "comparison", "how to", "news", "meilleur", "les "]):
        return False
    if sum(1 for c in name if c.isspace()) > 4:
        return False
    if any(token in lowered for token in GENERIC_TOOL_NAME_TOKENS):
        return False
    return True


def is_valid_tool_url(url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False

    if parsed.scheme not in {"http", "https"}:
        return False

    host = (parsed.hostname or "").lower().removeprefix("www.")
    if not host or "." not in host:
        return False

    if host in DISALLOWED_TOOL_HOSTS:
        return False

    lowered_url = url.lower()
    if any(marker in lowered_url for marker in ["/search?", "?q=", "duckduckgo.com", "google.com/search"]):
        return False

    return True


def passes_tool_quality_gate(tool: dict) -> bool:
    name = normalize_tool_name(tool.get("name", ""))
    url = (tool.get("url") or "").strip()

    if not is_likely_tool_name(name):
        return False
    if not is_valid_tool_url(url):
        return False
    return True


def ask_gemini(prompt: str) -> str:
    """Appel Gemini avec fallback automatique entre modèles (voir GEMINI_MODELS)."""
    tracer = get_tracer()
    tracer.trace_gemini_prompt(prompt)

    if tracer.is_dry_run:
        print("\n[DRY-RUN] Skipping Gemini API call.")
        tracer.log("DRY_RUN", "GEMINI", "Skipped Gemini call in dry-run mode", {})
        return "[]"

    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set. Skipping LLM step.")
        tracer.log("ERROR", "GEMINI", "GEMINI_API_KEY not set", {})
        return "[]"

    genai.configure(api_key=GEMINI_API_KEY)

    for idx, model_name in enumerate(GEMINI_MODELS):
        is_last = idx == len(GEMINI_MODELS) - 1
        print(f"Trying model {model_name} ({idx + 1}/{len(GEMINI_MODELS)})...")
        model = genai.GenerativeModel(model_name)

        def _generate_once() -> str:
            response = model.generate_content(prompt)
            return response.text

        try:
            return _generate_once()
        except google_api_exceptions.ResourceExhausted as e:
            print(
                f"Gemini quota exceeded for {model_name} (ResourceExhausted). "
                f"Waiting {GEMINI_RETRY_WAIT_SECONDS}s before one retry: {e}"
            )
            tracer.log("WARNING", "GEMINI", "Quota exceeded, retrying", {"model": model_name})
            time.sleep(GEMINI_RETRY_WAIT_SECONDS)
            try:
                return _generate_once()
            except google_api_exceptions.ResourceExhausted:
                if is_last:
                    print(f"All models exhausted. Skipping LLM step.")
                    tracer.log("ERROR", "GEMINI", "All models exhausted", {})
                    return "[]"
                print(f"Quota still exceeded for {model_name}. Falling back to next model.")
                continue
            except (google_api_exceptions.GoogleAPICallError, Exception) as retry_err:
                if is_last:
                    print(f"Error after retry on {model_name}: {retry_err}. Skipping LLM step.")
                    tracer.log("ERROR", "GEMINI", f"Error after retry: {retry_err}", {})
                    return "[]"
                print(f"Error after retry on {model_name}: {retry_err}. Falling back to next model.")
                continue
        except google_api_exceptions.GoogleAPICallError as e:
            if is_last:
                print(f"Gemini API call failed on {model_name}: {e}. Skipping LLM step.")
                tracer.log("ERROR", "GEMINI", f"API call failed: {e}", {})
                return "[]"
            print(f"Gemini API call failed on {model_name}: {e}. Falling back to next model.")
            continue
        except Exception as e:
            if is_last:
                print(f"Unexpected error on {model_name}: {e}. Skipping LLM step.")
                tracer.log("ERROR", "GEMINI", f"Unexpected error: {e}", {})
                return "[]"
            print(f"Unexpected error on {model_name}: {e}. Falling back to next model.")
            continue

    return "[]"


def extract_new_tools(search_results: str, existing_names: list[str], data: dict = None) -> list[dict]:
    """Demande à Gemini d'identifier les nouveaux outils."""
    tracer = get_tracer()
    existing_str = ", ".join(existing_names[:50])

    # Build category reference from actual data structure
    category_ref = ""
    if data and "categories" in data:
        category_ref = "\n\nCATÉGORIES DISPONIBLES :\n"
        for cat in data["categories"]:
            cat_name = cat.get("name", "")
            subs = [s.get("name", "") for s in cat.get("subcategories", [])]
            category_ref += f"- {cat_name}: {', '.join(subs)}\n"
    else:
        category_ref = "(Pas de catégories disponibles - l'outil sera assigné à la première catégorie)"

    prompt = f"""Tu es un expert en outils IA. Analyse ces résultats de recherche et identifie des outils IA qui ne sont PAS déjà dans la liste existante.

IMPORTANT : Les variantes d'un produit existant sont des OUTILS DISTINCTS :
- Si "Gemini" existe, "Gemini CLI" est un nouvel outil (variante CLI/terminal)
- Si "Claude" existe, "Claude for VSCode" est un nouvel outil (extension/intégration)
- Les applications web, CLI, extensions, plugins d'une même plateforme sont des outils différents
- Inclus les variantes même si le produit principal est connu

LISTE EXISTANTE (noms à exclure - ne pas ignorer les variantes) :
{existing_str}

RÉSULTATS DE RECHERCHE :
{search_results}

{category_ref}

Retourne UNIQUEMENT un tableau JSON valide (sans markdown, sans commentaire) avec les nouveaux outils trouvés, format :
[
  {{
    "name": "Nom de l'outil",
    "provider": "Entreprise ou vide",
    "url": "https://...",
    "desc": "Description courte en français (max 50 chars)",
    "category_id": "ID de la catégorie ou vide",
    "subcategory_name": "Nom de la sous-catégorie existante"
  }}
]

Règles :
- Maximum 10 outils les plus pertinents
- Uniquement des outils réels avec URL valide et fonctionnel
- Les variantes, extensions, CLI, plugins d'un produit connu = nouveaux outils (ne pas les exclure)
- Les doublons stricts à exclure : même nom ET même type d'accès
- Utilise les noms de sous-catégories existants si possible
- category_id doit correspondre à une catégorie existante
- subcategory_name doit correspondre à une sous-catégorie existante pour le category_id choisi
- Si aucun nouvel outil pertinent, retourne []
"""

    raw = ask_gemini(prompt)

    # Nettoyer la réponse (parfois Gemini ajoute des backticks)
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        tools = json.loads(raw)
        if isinstance(tools, list):
            tracer.log("SUCCESS", "EXTRACTION", f"Extracted {len(tools)} tools via Gemini", {"count": len(tools)})
            return tools
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nRaw: {raw[:300]}")
        tracer.log("ERROR", "EXTRACTION", f"JSON parse error: {e}", {})
    return []


def extract_tools_from_results_fallback(search_results: list[dict], existing_names: list[str], profile: str) -> list[dict]:
    tracer = get_tracer()
    extracted: list[dict] = []
    seen = set(existing_names)

    # First pass: detect known CLI tools from raw search evidence.
    if profile == "aicliapps":
        corpus = "\n".join(
            f"{hit.get('title', '')} {hit.get('body', '')} {hit.get('url', '')} {hit.get('query', '')}".lower()
            for hit in search_results
        )
        for known_tool in KNOWN_CLI_TOOL_CATALOG:
            if any(keyword in corpus for keyword in known_tool["keywords"]):
                lowered_name = known_tool["name"].lower()
                if lowered_name in seen:
                    continue
                extracted.append({
                    "name": known_tool["name"],
                    "provider": known_tool["provider"],
                    "url": known_tool["url"],
                    "desc": "Detecte via resultats DuckDuckGo CLI",
                    "category_id": known_tool["category_id"],
                    "subcategory_name": known_tool["subcategory_name"],
                    "source_text": corpus,
                })
                tracer.log("DEBUG", "FALLBACK_DETECTION", f"Detected known CLI tool: {known_tool['name']}", {})
                seen.add(lowered_name)
            if len(extracted) >= 10:
                return extracted

        # Keep CLI profile clean: if at least one known CLI tool was detected,
        # stop here instead of adding noisy article titles.
        if extracted:
            tracer.log("INFO", "FALLBACK_EXTRACTION", f"Found {len(extracted)} CLI tools via keyword matching", {"count": len(extracted)})
            return extracted

    for hit in search_results:
        title = hit.get("title", "")
        body = hit.get("body", "")
        url = hit.get("url", "")
        query = hit.get("query", "")
        if not url or is_excluded_host(url):
            continue

        name = extract_name_from_title(title)
        if not is_likely_tool_name(name):
            continue
        if profile == "aicliapps" and not any(token in f"{title} {body} {query}".lower() for token in ["cli", "terminal", "command", "shell", "agent", "devops", "sre", "llm"]):
            continue
        lowered_name = name.lower()
        if lowered_name in seen:
            continue

        host = (urlparse(url).hostname or "").lower().removeprefix("www.")
        provider = host.split(".")[0].capitalize() if host else ""
        desc = normalize_tool_name(body)[:90]

        tool = {
            "name": name,
            "provider": provider,
            "url": url,
            "desc": desc,
            "category_id": "",
            "subcategory_name": "",
            "source_text": f"{title} {body} {query}",
        }

        if profile == "aicliapps":
            category_id, sub_name = infer_aicliapps_category(tool["source_text"])
            tool["category_id"] = category_id
            tool["subcategory_name"] = sub_name

        extracted.append(tool)
        seen.add(lowered_name)

        if len(extracted) >= 10:
            break

    tracer.log("INFO", "FALLBACK_EXTRACTION", f"Extracted {len(extracted)} tools via title/body parsing", {"count": len(extracted)})
    return extracted


def add_tools_to_data(data: dict, new_tools: list[dict], profile: str) -> int:
    """Ajoute les nouveaux outils dans la structure JSON."""
    tracer = get_tracer()
    added = 0
    existing_names = get_existing_names(data)

    for tool in new_tools:
        name = tool.get("name", "").strip()

        if not name or name.lower() in existing_names:
            tracer.trace_tool_skipped(name, "duplicate")
            continue

        if not passes_tool_quality_gate(tool):
            print(f"Skipped low-confidence candidate: {name or '[no-name]'}")
            tracer.trace_tool_skipped(name or "[no-name]", "quality_gate_failed")
            continue

        target_cat, sub_name = resolve_category_and_subcategory(data, tool, profile)
        tracer.trace_category_resolution(name, target_cat.get("name", ""), sub_name)

        # Trouver la sous-catégorie valide
        target_sub = None
        for sub in target_cat.get("subcategories", []):
            if sub["name"].lower() == sub_name.lower():
                target_sub = sub
                break

        if not target_sub:
            fallback_sub_name = target_cat.get("subcategories", [{}])[0].get("name", "Nouveaux outils")
            for sub in target_cat.get("subcategories", []):
                if sub.get("name", "").lower() == fallback_sub_name.lower():
                    target_sub = sub
                    break
            if not target_sub:
                target_sub = {"name": fallback_sub_name, "icon": "", "tools": []}
                target_cat.setdefault("subcategories", []).append(target_sub)

        # Ajouter l'outil
        target_sub["tools"].append({
            "name": name,
            "provider": tool.get("provider", ""),
            "url": tool.get("url", "#"),
            "desc": tool.get("desc", ""),
            "new": True,
        })
        existing_names.append(name.lower())
        added += 1
        print(f"Added: {name} -> {target_cat['name']} / {target_sub['name']}")
        tracer.trace_tool_added(name, target_cat.get("name", ""), target_sub.get("name", ""))

    return added


def main():
    args = parse_args()
    profile = args.profile

    # Initialize tracer
    tracer = initialize_tracer(
        enabled=args.trace or args.dry_run,
        output_file=args.trace_output,
        dry_run=args.dry_run
    )

    tracer.trace_start(profile, [])  # Will be updated with queries below

    cfg = PROFILE_CONFIG[profile]
    tools_file = cfg["tools_file"]
    query_map = load_search_queries()
    search_queries = query_map[profile]

    # Update trace start with actual queries
    tracer.trace_log.clear()  # Clear placeholder
    tracer.trace_start(profile, search_queries)

    if profile == "aicliapps":
        # For CLI apps, rebuild from query evidence only.
        data = build_aicliapps_dataset(search_queries)
    else:
        ensure_tools_file(profile, search_queries)
        data = load_tools(tools_file)

    print("Searching for new AI tools...")
    print(f"Profile: {profile}")
    existing = get_existing_names(data)
    print(f"   {len(existing)} existing tools loaded")

    search_results = search_new_tools(search_queries)
    print(f"   {len(search_results)} search results collected")
    search_context = format_search_results_for_llm(search_results)
    tracer.trace_search_results_formatted(search_context)

    print("Asking Gemini to identify new tools...")
    new_tools = extract_new_tools(search_context, existing, data)
    if new_tools:
        tracer.trace_tool_extraction("gemini_extraction", new_tools)
    else:
        print("No valid Gemini extraction. Falling back to query-only extraction...")
        new_tools = extract_tools_from_results_fallback(search_results, existing, profile)
        tracer.trace_tool_extraction("fallback_extraction", new_tools)
    print(f"   {len(new_tools)} candidates found")

    added = 0
    if new_tools:
        added = add_tools_to_data(data, new_tools, profile)
        print(f"{added} new tools added")
        tracer.trace_json_update_summary(added, len(existing))

        # Skip save in dry-run mode
        if not tracer.is_dry_run:
            save_tools(data, profile, tools_file, search_queries)
        else:
            print(f"\n[DRY-RUN] Would save {added} new tools to {tools_file.name}")
            tracer.log("DRY_RUN", "SAVE", f"Would save to {tools_file.name}", {"added": added})
    else:
        print("No new tools to add, updating date only")
        tracer.trace_json_update_summary(0, len(existing))

        if not tracer.is_dry_run:
            save_tools(data, profile, tools_file, search_queries)
        else:
            print(f"\n[DRY-RUN] Would update metadata in {tools_file.name}")
            tracer.log("DRY_RUN", "SAVE", f"Would update {tools_file.name}", {})

    tracer.trace_end(added, profile)
    tracer.print_summary()


if __name__ == "__main__":
    main()
