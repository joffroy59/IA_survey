#!/usr/bin/env python3
"""
seed_profiles.py - Seed non-general profiles with tools from general profile
"""

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent

# Load general tools
general_file = ROOT / "data" / "tools.json"
with open(general_file, "r", encoding="utf-8") as f:
    general_data = json.load(f)

# Get all tools from general profile flattened
all_general_tools = []
for cat in general_data.get("categories", []):
    for sub in cat.get("subcategories", []):
        all_general_tools.extend(sub.get("tools", []))

print(f"Loaded {len(all_general_tools)} tools from general profile\n")

# Get list of all profile JSON files to seed
profiles_to_seed = ["enterprise", "discovery", "ragdev", "agentdev", "vscode", "newrag", "cowork", "ocr", "dococr"]

for profile_name in profiles_to_seed:
    profile_file = ROOT / "data" / f"tools-{profile_name}.json"

    with open(profile_file, "r", encoding="utf-8") as f:
        profile_data = json.load(f)

    # Distribute tools across profile's subcategories
    tool_index = 0
    tool_count = 0
    for cat in profile_data.get("categories", []):
        for sub in cat.get("subcategories", []):
            # Add 2-3 tools to each subcategory
            tools_to_add = all_general_tools[tool_index:tool_index+3]
            sub["tools"] = tools_to_add
            tool_index = (tool_index + 3) % len(all_general_tools)  # Cycle through tools
            tool_count += len(tools_to_add)
            if tools_to_add:
                print(f"  {profile_name}: {cat['name']} > {sub['name']} <- added {len(tools_to_add)} tools")

    # Update metadata
    now_iso = datetime.now().isoformat(timespec="milliseconds").replace("T", " ")
    profile_data["meta"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    if "page_history" not in profile_data["meta"]:
        profile_data["meta"]["page_history"] = []

    profile_data["meta"]["page_history"].insert(0, {
        "generated_at": now_iso,
        "tool_count": tool_count
    })
    profile_data["meta"]["page_history"] = profile_data["meta"]["page_history"][:10]

    # Save updated profile
    with open(profile_file, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)

    print(f"✓ {profile_file.name} seeded with {tool_count} tools\n")

print("✅ All profiles seeded successfully!")
