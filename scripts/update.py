#!/usr/bin/env python3
"""
update.py — Recherche de nouveaux outils IA et mise à jour de tools.json
APIs gratuites : DuckDuckGo (search) + Google Gemini Flash (LLM)
"""

import json
import os
import sys
import time
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
TOOLS_FILE = ROOT / "data" / "tools.json"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

SEARCH_QUERIES = [
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

MAX_SEARCH_RESULTS = 15  # par requête


def load_tools() -> dict:
    with open(TOOLS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tools(data: dict):
    data["meta"]["last_updated"] = date.today().isoformat()
    with open(TOOLS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"tools.json saved ({date.today()})")


def get_existing_names(data: dict) -> list[str]:
    names = []
    for cat in data["categories"]:
        for sub in cat.get("subcategories", []):
            for tool in sub.get("tools", []):
                names.append(tool["name"].lower())
    return names


def search_new_tools() -> str:
    """DuckDuckGo search — no API key required."""
    results = []
    with DDGS() as ddgs:
        for query in SEARCH_QUERIES:
            try:
                response = ddgs.text(query, max_results=MAX_SEARCH_RESULTS)
                print(f"Search for '{query}")
                print(f"Result Search '{response}")
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
    print("Searching for new AI tools...")
    data = load_tools()
    existing = get_existing_names(data)
    print(f"   {len(existing)} existing tools loaded")

    search_results = search_new_tools()
    print(f"   {len(search_results.splitlines())} search results collected")

    print("Asking Gemini to identify new tools...")
    new_tools = extract_new_tools(search_results, existing)
    print(f"   {len(new_tools)} candidates found")

    if new_tools:
        added = add_tools_to_data(data, new_tools)
        print(f"{added} new tools added")
        save_tools(data)
    else:
        print("No new tools to add, updating date only")
        save_tools(data)


if __name__ == "__main__":
    main()
