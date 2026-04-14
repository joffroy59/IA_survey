#!/usr/bin/env python3
"""
generate.py — Génère index.html depuis data/tools.json
"""

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent
TOOLS_FILE = ROOT / "data" / "tools.json"
OUTPUT = ROOT / "index.html"

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{subtitle}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0a0a0f;
      --surface: #111118;
      --surface2: #1a1a24;
      --border: #2a2a3a;
      --accent: #6c63ff;
      --accent2: #00d4aa;
      --text: #e8e8f0;
      --muted: #8888a0;
      --new: #ff6b6b;
      --radius: 12px;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: 'Space Grotesk', sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
      background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(108,99,255,0.15) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80% 80%, rgba(0,212,170,0.08) 0%, transparent 50%);
    }}

    /* ── Header ── */
    header {{
      text-align: center;
      padding: 60px 24px 40px;
      position: relative;
    }}
    header::after {{
      content: '';
      display: block;
      width: 120px;
      height: 2px;
      background: linear-gradient(90deg, transparent, var(--accent), var(--accent2), transparent);
      margin: 24px auto 0;
    }}
    .header-badge {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--accent2);
      background: rgba(0,212,170,0.1);
      border: 1px solid rgba(0,212,170,0.25);
      padding: 4px 12px;
      border-radius: 20px;
      margin-bottom: 20px;
      letter-spacing: 0.08em;
    }}
    h1 {{
      font-size: clamp(28px, 5vw, 48px);
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 30%, var(--accent));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      line-height: 1.15;
    }}
    .subtitle {{
      margin-top: 12px;
      color: var(--muted);
      font-size: 16px;
    }}
    .update-info {{
      margin-top: 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: var(--muted);
    }}
    .update-info span {{ color: var(--accent2); }}

    /* ── Nav tabs ── */
    nav {{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      gap: 8px;
      padding: 0 24px 32px;
      max-width: 900px;
      margin: 0 auto;
    }}
    .nav-tab {{
      font-size: 13px;
      font-weight: 500;
      padding: 7px 16px;
      border-radius: 20px;
      background: var(--surface);
      border: 1px solid var(--border);
      color: var(--muted);
      cursor: pointer;
      transition: all 0.2s;
      text-decoration: none;
    }}
    .nav-tab:hover, .nav-tab.active {{
      background: var(--accent);
      border-color: var(--accent);
      color: #fff;
    }}

    /* ── Main layout ── */
    main {{
      max-width: 1100px;
      margin: 0 auto;
      padding: 0 24px 80px;
    }}

    /* ── Category section ── */
    .category {{
      margin-bottom: 48px;
      display: none;
    }}
    .category.visible {{ display: block; }}

    .category-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 24px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border);
    }}
    .category-icon {{
      font-size: 28px;
      width: 48px;
      height: 48px;
      display: flex;
      align-items: center;
      justify-content: center;
      background: var(--surface2);
      border-radius: 12px;
      border: 1px solid var(--border);
    }}
    .category-title {{
      font-size: 22px;
      font-weight: 700;
      letter-spacing: -0.01em;
    }}

    /* ── Subcategory ── */
    .subcategory {{
      margin-bottom: 28px;
    }}
    .subcategory-title {{
      font-size: 13px;
      font-weight: 600;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.1em;
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .subcategory-title::after {{
      content: '';
      flex: 1;
      height: 1px;
      background: var(--border);
    }}

    /* ── Tools grid ── */
    .tools-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 10px;
    }}
    .tool-card {{
      display: flex;
      flex-direction: column;
      gap: 4px;
      padding: 14px 16px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      text-decoration: none;
      transition: all 0.18s ease;
      position: relative;
      overflow: hidden;
    }}
    .tool-card:hover {{
      border-color: var(--accent);
      background: var(--surface2);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(108,99,255,0.15);
    }}
    .tool-card.is-new {{
      border-color: rgba(255,107,107,0.3);
    }}
    .tool-card.is-new::before {{
      content: 'NEW';
      position: absolute;
      top: 8px;
      right: 8px;
      font-size: 9px;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      color: var(--new);
      background: rgba(255,107,107,0.1);
      padding: 2px 6px;
      border-radius: 4px;
      letter-spacing: 0.08em;
    }}
    .tool-name {{
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
    }}
    .tool-provider {{
      font-size: 11px;
      color: var(--accent2);
      font-family: 'JetBrains Mono', monospace;
    }}
    .tool-desc {{
      font-size: 12px;
      color: var(--muted);
      margin-top: 2px;
    }}

    /* ── Footer ── */
    footer {{
      text-align: center;
      padding: 32px;
      color: var(--muted);
      font-size: 13px;
      border-top: 1px solid var(--border);
      font-family: 'JetBrains Mono', monospace;
    }}
    footer a {{ color: var(--accent2); text-decoration: none; }}

    @media (max-width: 600px) {{
      .tools-grid {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>

<header>
  <div class="header-badge">🤖 Auto-updated by AI · {today}</div>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="update-info">Dernière mise à jour : <span>{last_updated}</span></p>
</header>

<nav>
  <a class="nav-tab active" href="#" data-cat="all">Tout voir</a>
  {nav_tabs}
</nav>

<main>
  {categories_html}
</main>

<footer>
  Généré automatiquement par GitHub Actions + Gemini AI · 
  <a href="https://github.com/{repo_name}" target="_blank">Voir sur GitHub</a>
</footer>

<script>
  const tabs = document.querySelectorAll('.nav-tab');
  const categories = document.querySelectorAll('.category');

  tabs.forEach(tab => {{
    tab.addEventListener('click', (e) => {{
      e.preventDefault();
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      const cat = tab.dataset.cat;
      categories.forEach(c => {{
        c.classList.toggle('visible', cat === 'all' || c.dataset.id === cat);
      }});
    }});
  }});

  // Show all on load
  categories.forEach(c => c.classList.add('visible'));
</script>

</body>
</html>"""


def render_tool(tool: dict) -> str:
    is_new = ' is-new' if tool.get("new") else ""
    provider = f'<div class="tool-provider">{tool["provider"]}</div>' if tool.get("provider") else ""
    desc = f'<div class="tool-desc">{tool["desc"]}</div>' if tool.get("desc") else ""
    return f"""
      <a class="tool-card{is_new}" href="{tool['url']}" target="_blank" rel="noopener">
        <div class="tool-name">{tool['name']}</div>
        {provider}
        {desc}
      </a>"""


def render_subcategory(sub: dict) -> str:
    tools_html = "\n".join(render_tool(t) for t in sub.get("tools", []))
    icon = sub.get("icon", "")
    return f"""
    <div class="subcategory">
      <div class="subcategory-title">{icon} {sub['name']}</div>
      <div class="tools-grid">
        {tools_html}
      </div>
    </div>"""


def render_category(cat: dict) -> str:
    subs_html = "\n".join(render_subcategory(s) for s in cat.get("subcategories", []))
    return f"""
  <section class="category" data-id="{cat['id']}">
    <div class="category-header">
      <div class="category-icon">{cat['icon']}</div>
      <div class="category-title">{cat['name']}</div>
    </div>
    {subs_html}
  </section>"""


def generate():
    with open(TOOLS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    cats = data["categories"]

    nav_tabs = "\n  ".join(
        f'<a class="nav-tab" href="#" data-cat="{c["id"]}">{c["icon"]} {c["name"]}</a>'
        for c in cats
    )
    categories_html = "\n".join(render_category(c) for c in cats)

    repo_name = "VOTRE-USERNAME/ai-toolbox"  # remplacer

    html = HTML_TEMPLATE.format(
        title=meta["title"],
        subtitle=meta["subtitle"],
        today=date.today().strftime("%d/%m/%Y"),
        last_updated=meta.get("last_updated", ""),
        nav_tabs=nav_tabs,
        categories_html=categories_html,
        repo_name=repo_name,
    )

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ index.html generated ({OUTPUT})")


if __name__ == "__main__":
    generate()
