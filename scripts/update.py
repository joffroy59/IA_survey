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
from datetime import date
from pathlib import Path

# ── Dépendances ──────────────────────────────────────────────────────────────
try:
    from ddgs import DDGS
    import google.generativeai as genai
except ImportError:
    print("Installing dependencies...")
    os.system("pip install ddgs google-generativeai --quiet")
    from ddgs import DDGS
    import google.generativeai as genai

# ── Config ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

GENERAL_SEARCH_QUERIES = [
    "new AI tools 2026 site:producthunt.com OR site:theresanaiforthat.com",
    "new AI tools 2026 site:futurepedia.io OR site:uneed.best",
    "new AI agentic workflows site:news.ycombinator.com 2026",
    "best new AI coding tools 2026 site:tldr.tech",
    "trending AI repositories 2026 site:github.com",
    "new AI image video audio tools 2026 site:the-decoder.com",
    "meilleurs outils IA agentique 2026",
    "state-of-the-art AI benchmarks April 2026",
    "best professional AI tools for developers 2026"
]

ENTERPRISE_SEARCH_QUERIES = [
    "RAG architecture tools enterprise 2026",
    "retrieval augmented generation frameworks production 2026",
    "best RAG tools open source vector database 2026",
    "LLM RAG pipeline production stack 2026",
    "AI agents frameworks enterprise automation 2026",
    "agentic workflows tools production AI agents 2026",
    "multi agent systems frameworks 2026 open source",
    "AI orchestration tools LangChain alternatives 2026",
    "AI developer tools enterprise coding assistant self hosted 2026",
    "secure AI coding tools for companies 2026",
    "on premise AI dev tools LLM enterprise 2026",
    "LLM infrastructure tools enterprise deployment 2026",
    "self hosted LLM stack enterprise vector db embedding 2026",
    "AI platform enterprise stack comparison 2026",
    "AI use cases enterprise automation internal tools 2026",
    "AI for business process automation tools 2026",
    "LLM internal knowledge base chatbot enterprise 2026",
    "secure AI tools enterprise GDPR LLM privacy 2026",
    "on premise AI tools Europe compliance 2026",
    "AI tools enterprise site:github.com RAG OR agent",
    "AI infrastructure blog LLM stack 2026 site:medium.com OR site:substack.com",
    "Show HN enterprise AI tool RAG agent site:news.ycombinator.com",
    "outils IA entreprise RAG agentique France 2026",
    "plateforme IA entreprise Europe LLM open source",
]

OPTIMIZED_GENERAL_SEARCH_QUERIES = [
    "latest AI tools 2026 site:theresanaiforthat.com OR site:futurepedia.io",
    "new AI startups tools 2026 site:producthunt.com AI",
    "trending AI tools this week 2026 site:theresanaiforthat.com",
    "best new AI tools April 2026 site:futurepedia.io",
    "trending AI repositories 2026 site:github.com stars >100",
    "AI agent open source projects 2026 site:github.com",
    "Show HN AI tool 2026 site:news.ycombinator.com",
    "AI agent discussion 2026 site:news.ycombinator.com",
    "AI coding assistant tools 2026",
    "AI video generation tools 2026",
    "AI automation agent tools 2026",
    "meilleurs outils IA 2026 nouveautés",
    "outils IA productivité 2026",
    "state of the art AI tools 2026 blog",
    "new AI workflows automation tools 2026",
]

PROFILE_CONFIG = {
    "general": {
        "tools_file": ROOT / "data" / "tools.json",
        "page_name": "general",
        "page_label": "Panorama Generaliste",
        "page_description": "Vue complete des meilleurs outils IA grand public et pro.",
        "search_queries": GENERAL_SEARCH_QUERIES,
    },
    "enterprise": {
        "tools_file": ROOT / "data" / "tools-enterprise.json",
        "page_name": "enterprise",
        "page_label": "Panorama Enterprise",
        "page_description": "Focus RAG, agents, infra, securite et cas d'usage entreprise.",
        "search_queries": ENTERPRISE_SEARCH_QUERIES,
    },
    "discovery": {
        "tools_file": ROOT / "data" / "tools-discovery.json",
        "page_name": "discovery",
        "page_label": "Panorama Decouverte",
        "page_description": "Version optimisee des requetes generales pour detecter les nouveautes.",
        "search_queries": OPTIMIZED_GENERAL_SEARCH_QUERIES,
    },
}

MAX_SEARCH_RESULTS = 15  # par requête


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update AI tools datasets")
    parser.add_argument(
        "--profile",
        choices=sorted(PROFILE_CONFIG.keys()),
        default="general",
        help="Dataset profile to update",
    )
    return parser.parse_args()


def ensure_tools_file(profile: str):
    cfg = PROFILE_CONFIG[profile]
    tools_file = cfg["tools_file"]
    if tools_file.exists():
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
    base_data["meta"]["search_queries"] = cfg["search_queries"]

    with open(tools_file, "w", encoding="utf-8") as f:
        json.dump(base_data, f, ensure_ascii=False, indent=2)
    print(f"Created missing dataset: {tools_file}")


def load_tools(tools_file: Path) -> dict:
    with open(tools_file, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tools(data: dict, profile: str, tools_file: Path):
    cfg = PROFILE_CONFIG[profile]
    data["meta"]["last_updated"] = date.today().isoformat()
    data["meta"]["page_name"] = cfg["page_name"]
    data["meta"]["page_label"] = cfg["page_label"]
    data["meta"]["page_description"] = cfg["page_description"]
    data["meta"]["search_queries"] = cfg["search_queries"]
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


def search_new_tools(search_queries: list[str]) -> str:
    """DuckDuckGo search — no API key required."""
    results = []
    with DDGS() as ddgs:
        for query in search_queries:
            try:
                response = ddgs.text(query, max_results=MAX_SEARCH_RESULTS)
                print(f"Search for '{query}'")
                hits = list(response)
                for h in hits:
                    results.append(f"- {h['title']}: {h['body']} ({h['href']})")
                time.sleep(1)  # rate limit courtesy
            except Exception as e:
                print(f"Search error for '{query}': {e}")
    return "\n".join(results[:60])  # limit context size


def ask_gemini(prompt: str) -> str:
    """Appel Gemini Flash — free tier: 1500 req/day."""
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not set. Skipping LLM step.")
        return "[]"

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


def extract_new_tools(search_results: str, existing_names: list[str]) -> list[dict]:
    """Demande à Gemini d'identifier les nouveaux outils."""
    existing_str = ", ".join(existing_names[:50])

    prompt = f"""Tu es un expert en outils IA. Analyse ces résultats de recherche et identifie des outils IA qui ne sont PAS déjà dans la liste existante.

LISTE EXISTANTE (noms à exclure) :
{existing_str}

RÉSULTATS DE RECHERCHE :
{search_results}

Retourne UNIQUEMENT un tableau JSON valide (sans markdown, sans commentaire) avec les nouveaux outils trouvés, format :
[
  {{
    "name": "Nom de l'outil",
    "provider": "Entreprise ou vide",
    "url": "https://...",
    "desc": "Description courte en français (max 50 chars)",
    "category_id": "generiques|specialisees|images|code|audio|video",
    "subcategory_name": "Nom de la sous-catégorie existante ou nouvelle"
  }}
]

Règles :
- Maximum 10 outils les plus pertinents
- Uniquement des outils réels avec URL valide
- Pas de doublons avec la liste existante
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
            return tools
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}\nRaw: {raw[:300]}")
    return []


def add_tools_to_data(data: dict, new_tools: list[dict]) -> int:
    """Ajoute les nouveaux outils dans la structure JSON."""
    added = 0
    existing_names = get_existing_names(data)

    for tool in new_tools:
        name = tool.get("name", "").strip()
        cat_id = tool.get("category_id", "")
        sub_name = tool.get("subcategory_name", "Nouveaux outils")

        if not name or name.lower() in existing_names:
            continue

        # Trouver la catégorie cible
        target_cat = None
        for cat in data["categories"]:
            if cat["id"] == cat_id:
                target_cat = cat
                break

        # Fallback : première catégorie
        if not target_cat:
            target_cat = data["categories"][0]

        # Trouver ou créer la sous-catégorie
        target_sub = None
        for sub in target_cat.get("subcategories", []):
            if sub["name"].lower() == sub_name.lower():
                target_sub = sub
                break

        if not target_sub:
            target_sub = {"name": sub_name, "icon": "", "tools": []}
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

    return added


def main():
    args = parse_args()
    profile = args.profile
    cfg = PROFILE_CONFIG[profile]
    tools_file = cfg["tools_file"]

    ensure_tools_file(profile)

    print("Searching for new AI tools...")
    print(f"Profile: {profile}")
    data = load_tools(tools_file)
    existing = get_existing_names(data)
    print(f"   {len(existing)} existing tools loaded")

    search_results = search_new_tools(cfg["search_queries"])
    print(f"   {len(search_results.splitlines())} search results collected")

    print("Asking Gemini to identify new tools...")
    new_tools = extract_new_tools(search_results, existing)
    print(f"   {len(new_tools)} candidates found")

    if new_tools:
        added = add_tools_to_data(data, new_tools)
        print(f"{added} new tools added")
        save_tools(data, profile, tools_file)
    else:
        print("No new tools to add, updating date only")
        save_tools(data, profile, tools_file)


if __name__ == "__main__":
    main()
