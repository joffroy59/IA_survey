#!/usr/bin/env python3
"""
seed_profiles.py - Seed non-general profiles with profile-specific tools.

The previous version copied the same sequential chunks from the general profile
to every page, which made multiple pages show the same tools.
"""

import json
from copy import deepcopy
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent

PROFILES_TO_SEED = [
    "enterprise",
    "discovery",
    "ragdev",
    "agentdev",
    "vscode",
    "newrag",
    "cowork",
    "ocr",
    "dococr",
]

PROFILE_KEYWORDS = {
    "enterprise": [
        "enterprise", "security", "api", "workflow", "automation", "platform", "team", "business", "crm", "salesforce", "microsoft", "azure",
    ],
    "discovery": [
        "search", "discover", "research", "web", "insight", "trend", "analysis", "assistant", "chat", "knowledge", "idea",
    ],
    "ragdev": [
        "rag", "vector", "retrieval", "embedding", "database", "langchain", "llamaindex", "pinecone", "weaviate", "qdrant", "dev", "code",
    ],
    "agentdev": [
        "agent", "code", "developer", "dev", "ide", "github", "copilot", "cursor", "claude", "terminal", "automation",
    ],
    "vscode": [
        "vscode", "visual studio", "extension", "github", "copilot", "code", "developer", "dev", "debug", "lint",
    ],
    "newrag": [
        "rag", "knowledge", "retrieval", "agent", "orchestration", "memory", "pipeline", "vector", "search", "hybrid",
    ],
    "cowork": [
        "collab", "collaboration", "meeting", "workspace", "team", "project", "notion", "slack", "document", "productivity",
    ],
    "ocr": [
        "ocr", "document", "scan", "pdf", "image", "extract", "text", "invoice", "receipt", "recognition",
    ],
    "dococr": [
        "ocr", "document", "workflow", "classification", "form", "invoice", "compliance", "processing", "extraction", "enterprise",
    ],
}

PROFILE_TOOLS_PER_SUBCATEGORY = {
    "enterprise": 2,
    "discovery": 2,
    "ragdev": 2,
    "agentdev": 2,
    "vscode": 2,
    "newrag": 2,
    "cowork": 2,
    "ocr": 2,
    "dococr": 2,
}


def flatten_general_tools(general_data: dict) -> list[dict]:
    seen = set()
    tools: list[dict] = []
    for category in general_data.get("categories", []):
        for subcategory in category.get("subcategories", []):
            for tool in subcategory.get("tools", []):
                name = (tool.get("name") or "").strip().lower()
                if not name or name in seen:
                    continue
                seen.add(name)
                tools.append(tool)
    return tools


def score_tool(tool: dict, keywords: list[str]) -> int:
    haystack = " ".join(
        [
            str(tool.get("name", "")),
            str(tool.get("provider", "")),
            str(tool.get("desc", "")),
            str(tool.get("url", "")),
        ]
    ).lower()
    return sum(1 for kw in keywords if kw in haystack)


def select_tools_for_profile(
    all_tools: list[dict],
    profile_name: str,
    needed_count: int,
    profile_index: int,
) -> list[dict]:
    keywords = PROFILE_KEYWORDS.get(profile_name, [])
    scored = [(score_tool(tool, keywords), tool) for tool in all_tools]
    scored.sort(key=lambda item: (-item[0], item[1].get("name", "").lower()))
    ranked_tools = [tool for _, tool in scored]

    if not ranked_tools:
        return []

    offset = (profile_index * 5) % len(ranked_tools)
    stride = (profile_index % 5) + 1

    selected: list[dict] = []
    selected_names = set()
    cursor = 0
    max_iterations = len(ranked_tools) * 6

    while len(selected) < needed_count and cursor < max_iterations:
        idx = (offset + (cursor * stride)) % len(ranked_tools)
        tool = ranked_tools[idx]
        name = (tool.get("name") or "").lower()
        if name and name not in selected_names:
            selected.append(tool)
            selected_names.add(name)
        cursor += 1

    return selected


def main() -> None:
    general_file = ROOT / "data" / "tools.json"
    with open(general_file, "r", encoding="utf-8") as f:
        general_data = json.load(f)

    all_general_tools = flatten_general_tools(general_data)
    print(f"Loaded {len(all_general_tools)} unique tools from general profile\n")

    for profile_index, profile_name in enumerate(PROFILES_TO_SEED):
        profile_file = ROOT / "data" / f"tools-{profile_name}.json"

        with open(profile_file, "r", encoding="utf-8") as f:
            profile_data = json.load(f)

        subcategories = [
            sub
            for cat in profile_data.get("categories", [])
            for sub in cat.get("subcategories", [])
        ]
        tools_per_subcategory = PROFILE_TOOLS_PER_SUBCATEGORY.get(profile_name, 2)
        needed_count = len(subcategories) * tools_per_subcategory
        profile_tools = select_tools_for_profile(
            all_general_tools,
            profile_name,
            needed_count,
            profile_index,
        )

        tool_count = 0
        cursor = 0
        for cat in profile_data.get("categories", []):
            for sub in cat.get("subcategories", []):
                tools_to_add = [
                    deepcopy(t)
                    for t in profile_tools[cursor:cursor + tools_per_subcategory]
                ]
                sub["tools"] = tools_to_add
                cursor += tools_per_subcategory
                tool_count += len(tools_to_add)
                if tools_to_add:
                    print(
                        f"  {profile_name}: {cat['name']} > {sub['name']} "
                        f"<- added {len(tools_to_add)} tools"
                    )

        now = datetime.now()
        now_iso = now.isoformat(timespec="milliseconds").replace("T", " ")
        profile_data.setdefault("meta", {})
        profile_data["meta"]["last_updated"] = now.strftime("%Y-%m-%d")
        profile_data["meta"].setdefault("page_history", [])
        profile_data["meta"]["page_history"].insert(
            0,
            {
                "generated_at": now_iso,
                "tool_count": tool_count,
            },
        )
        profile_data["meta"]["page_history"] = profile_data["meta"]["page_history"][:10]

        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)

        print(f"✓ {profile_file.name} seeded with {tool_count} tools\n")

    print("✅ All profiles seeded successfully!")


if __name__ == "__main__":
    main()
