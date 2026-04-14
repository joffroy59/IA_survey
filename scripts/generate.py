#!/usr/bin/env python3
"""
generate.py — Génère index.html depuis data/tools.json
"""

import json
from datetime import date, datetime
from html import escape
from pathlib import Path

ROOT = Path(__file__).parent.parent

PAGE_CONFIGS = [
    {
        "slug": "general",
        "label": "Vue Generale",
        "data_file": ROOT / "data" / "tools.json",
        "output": ROOT / "index.html",
    },
    {
        "slug": "enterprise",
        "label": "Vue Enterprise",
        "data_file": ROOT / "data" / "tools-enterprise.json",
        "output": ROOT / "enterprise.html",
    },
    {
        "slug": "discovery",
        "label": "Vue Decouverte",
        "data_file": ROOT / "data" / "tools-discovery.json",
        "output": ROOT / "discovery.html",
    },
    {
      "slug": "ragdev",
      "label": "Vue RAG Pro + DevTools",
      "data_file": ROOT / "data" / "tools-ragdev.json",
      "output": ROOT / "ragdev.html",
    },
]

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
    .page-switcher {{
      margin-top: 20px;
      display: inline-flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
      padding: 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: rgba(17, 17, 24, 0.9);
    }}
    .page-link {{
      text-decoration: none;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 999px;
      border: 1px solid transparent;
      transition: all 0.2s;
    }}
    .page-link.active, .page-link:hover {{
      color: #fff;
      border-color: var(--accent);
      background: var(--accent);
    }}
    .page-meta {{
      margin: 20px auto 0;
      max-width: 820px;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: rgba(17, 17, 24, 0.85);
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      align-items: center;
      padding: 14px 16px;
    }}
    .page-meta-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.08em;
      color: var(--accent2);
      text-transform: uppercase;
    }}
    .page-meta-title {{
      font-weight: 700;
      font-size: 16px;
      margin-top: 4px;
    }}
    .page-meta-desc {{
      color: var(--muted);
      font-size: 13px;
      margin-top: 4px;
    }}
    .info-btn {{
      border: 1px solid var(--border);
      background: var(--surface2);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 10px;
      cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      transition: all 0.2s;
    }}
    .info-btn:hover {{
      border-color: var(--accent);
      color: #fff;
    }}
    .button-group {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
    }}
    .history-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }}
    .history-table thead {{
      background: var(--surface2);
    }}
    .history-table th {{
      text-align: left;
      padding: 10px 12px;
      font-weight: 600;
      font-size: 12px;
      text-transform: uppercase;
      color: var(--accent2);
      border-bottom: 1px solid var(--border);
    }}
    .history-table td {{
      padding: 10px 12px;
      font-size: 13px;
      border-bottom: 1px solid var(--border);
    }}
    .history-table tr:hover {{
      background: rgba(108,99,255,0.05);
    }}
    .history-date {{
      font-family: 'JetBrains Mono', monospace;
      color: var(--accent2);
    }}
    .history-count {{
      text-align: right;
      color: var(--muted);
    }}

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

    .modal-overlay {{
      position: fixed;
      inset: 0;
      background: rgba(5, 5, 8, 0.72);
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      z-index: 99;
    }}
    .modal-overlay.open {{ display: flex; }}
    .modal {{
      width: min(920px, 100%);
      max-height: 82vh;
      overflow: auto;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45);
      padding: 18px 20px;
    }}
    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }}
    .modal-title {{
      font-size: 18px;
      font-weight: 700;
    }}
    .close-btn {{
      border: 1px solid var(--border);
      border-radius: 8px;
      background: var(--surface2);
      color: var(--text);
      padding: 7px 10px;
      cursor: pointer;
      font-size: 12px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .modal-meta {{
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 12px;
      font-family: 'JetBrains Mono', monospace;
    }}
    .query-list {{
      list-style: decimal inside;
      display: grid;
      gap: 8px;
    }}
    .query-list li {{
      color: var(--text);
      font-size: 13px;
      line-height: 1.45;
      border: 1px solid var(--border);
      background: var(--surface2);
      border-radius: 8px;
      padding: 8px 10px;
    }}

    @media (max-width: 600px) {{
      .tools-grid {{ grid-template-columns: 1fr 1fr; }}
      .page-meta {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<header>
  <div class="header-badge">🤖 Auto-updated by AI · {today}</div>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>
  <p class="update-info">Dernière mise à jour : <span>{last_updated}</span></p>
  <div class="page-switcher">{page_switcher}</div>
  <div class="page-meta">
    <div>
      <div class="page-meta-label">Type de page</div>
      <div class="page-meta-title">{page_label}</div>
      <div class="page-meta-desc">{page_description}</div>
    </div>
    <div class="button-group">
      <button class="info-btn" type="button" id="open-search-info">Sources</button>
      <button class="info-btn" type="button" id="open-history-info">Historique</button>
    </div>
  </div>
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

<div class="modal-overlay" id="search-modal" aria-hidden="true">
  <div class="modal" role="dialog" aria-modal="true" aria-label="Recherche utilisee">
    <div class="modal-header">
      <div class="modal-title">Requêtes de recherche utilisées</div>
      <button class="close-btn" type="button" id="close-search-info">Fermer</button>
    </div>
    <div class="modal-meta">Page: {page_label} · Dernière mise à jour: {last_updated}</div>
    <ol class="query-list">
      {search_queries_html}
    </ol>
  </div>
</div>

<div class="modal-overlay" id="history-modal" aria-hidden="true">
  <div class="modal" role="dialog" aria-modal="true" aria-label="Historique des versions">
    <div class="modal-header">
      <div class="modal-title">Historique des versions</div>
      <button class="close-btn" type="button" id="close-history-info">Fermer</button>
    </div>
    <div class="modal-meta">Page: {page_label} · Dernières 10 générations</div>
    <table class="history-table">
      <thead>
        <tr>
          <th>Date de génération</th>
          <th class="history-count">Outils détectés</th>
        </tr>
      </thead>
      <tbody>
        {history_html}
      </tbody>
    </table>
  </div>
</div>

<script>
  const tabs = document.querySelectorAll('.nav-tab');
  const categories = document.querySelectorAll('.category');
  const searchModal = document.getElementById('search-modal');
  const historyModal = document.getElementById('history-modal');
  const openSearchInfo = document.getElementById('open-search-info');
  const closeSearchInfo = document.getElementById('close-search-info');
  const openHistoryInfo = document.getElementById('open-history-info');
  const closeHistoryInfo = document.getElementById('close-history-info');

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

  // Search modal handlers
  openSearchInfo.addEventListener('click', () => {{
    searchModal.classList.add('open');
    searchModal.setAttribute('aria-hidden', 'false');
  }});

  closeSearchInfo.addEventListener('click', () => {{
    searchModal.classList.remove('open');
    searchModal.setAttribute('aria-hidden', 'true');
  }});

  // History modal handlers
  openHistoryInfo.addEventListener('click', () => {{
    historyModal.classList.add('open');
    historyModal.setAttribute('aria-hidden', 'false');
  }});

  closeHistoryInfo.addEventListener('click', () => {{
    historyModal.classList.remove('open');
    historyModal.setAttribute('aria-hidden', 'true');
  }});

  // Close modals on overlay click or Escape
  function closeAllModals() {{
    [searchModal, historyModal].forEach(m => {{
      m.classList.remove('open');
      m.setAttribute('aria-hidden', 'true');
    }});
  }}

  [searchModal, historyModal].forEach(modal => {{
    modal.addEventListener('click', (event) => {{
      if (event.target === modal) {{
        closeAllModals();
      }}
    }});
  }});

  document.addEventListener('keydown', (event) => {{
    if (event.key === 'Escape') {{
      closeAllModals();
    }}
  }});
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


def render_page_switcher(active_slug: str) -> str:
    links = []
    for cfg in PAGE_CONFIGS:
        href = cfg["output"].name
        classes = "page-link active" if cfg["slug"] == active_slug else "page-link"
        links.append(f'<a class="{classes}" href="{href}">{escape(cfg["label"])}</a>')
    return "\n    ".join(links)


def render_search_queries(search_queries: list[str]) -> str:
    if not search_queries:
        return "<li>Aucune requête enregistrée.</li>"
    return "\n      ".join(f"<li>{escape(q)}</li>" for q in search_queries)


def count_tools(categories: list[dict]) -> int:
    """Count total number of tools across all categories and subcategories."""
    total = 0
    for cat in categories:
        for sub in cat.get("subcategories", []):
            total += len(sub.get("tools", []))
    return total


def render_history(page_history: list[dict]) -> str:
    """Render history table rows."""
    if not page_history:
        return "<tr><td colspan='2' style='text-align: center; color: var(--muted);'>Aucun historique disponible</td></tr>"

    rows = []
    for entry in page_history:
        date_str = entry.get("date", "?")
        tool_count = entry.get("tool_count", 0)
        rows.append(f"""        <tr>
          <td class="history-date">{escape(str(date_str))}</td>
          <td class="history-count">{tool_count}</td>
        </tr>""")
    return "\n".join(rows)


def generate_page(page_cfg: dict):
    data_file = page_cfg["data_file"]
    output_file = page_cfg["output"]
    if not data_file.exists():
        print(f"Skipping {output_file.name}: missing {data_file.name}")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    cats = data["categories"]

    # Count tools and manage history
    tool_count = count_tools(cats)
    today_str = date.today().strftime("%Y-%m-%d")

    # Load existing history and add new entry
    page_history = meta.get("page_history", [])
    new_entry = {
        "date": today_str,
        "tool_count": tool_count
    }

    # Add new entry if it's a new date or update today's entry
    if page_history and page_history[-1]["date"] == today_str:
        page_history[-1] = new_entry
    else:
        page_history.append(new_entry)

    # Keep only last 10 entries
    page_history = page_history[-10:]

    # Update meta with new history
    meta["page_history"] = page_history

    # Save updated data file
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    nav_tabs = "\n  ".join(
        f'<a class="nav-tab" href="#" data-cat="{c["id"]}">{c["icon"]} {c["name"]}</a>'
        for c in cats
    )
    categories_html = "\n".join(render_category(c) for c in cats)
    page_label = meta.get("page_label", "Panorama Generaliste")
    page_description = meta.get(
        "page_description",
        "Vue complete des outils detectes par veille automatique.",
    )
    search_queries_html = render_search_queries(meta.get("search_queries", []))
    history_html = render_history(page_history)

    repo_name = "VOTRE-USERNAME/ai-toolbox"  # remplacer

    html = HTML_TEMPLATE.format(
        title=meta["title"],
        subtitle=meta["subtitle"],
        today=date.today().strftime("%d/%m/%Y"),
        last_updated=meta.get("last_updated", ""),
        page_switcher=render_page_switcher(meta.get("page_name", "general")),
        page_label=escape(page_label),
        page_description=escape(page_description),
        search_queries_html=search_queries_html,
        history_html=history_html,
        nav_tabs=nav_tabs,
        categories_html=categories_html,
        repo_name=repo_name,
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {output_file.name} generated ({output_file})")


def generate():
    for page_cfg in PAGE_CONFIGS:
        generate_page(page_cfg)


if __name__ == "__main__":
    generate()
