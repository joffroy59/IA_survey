#!/usr/bin/env python3
"""
generate.py — Génère index.html depuis data/tools.json
"""

import json
from datetime import date, datetime
from html import escape
from pathlib import Path
from urllib.parse import quote

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
    {
      "slug": "agentdev",
      "label": "Vue Agent Dev + IDE Tools",
      "data_file": ROOT / "data" / "tools-agentdev.json",
      "output": ROOT / "agentdev.html",
    },
    {
      "slug": "vscode",
      "label": "Vue VS Code",
      "data_file": ROOT / "data" / "tools-vscode.json",
      "output": ROOT / "vscode.html",
    },
    {
      "slug": "newrag",
      "label": "Vue New RAG",
      "data_file": ROOT / "data" / "tools-newrag.json",
      "output": ROOT / "newrag.html",
    },
    {
      "slug": "cowork",
      "label": "vue Claude Cowork",
      "data_file": ROOT / "data" / "tools-cowork.json",
      "output": ROOT / "cowork.html",
    },
    {
      "slug": "ocr",
      "label": "Vue OCR",
      "data_file": ROOT / "data" / "tools-ocr.json",
      "output": ROOT / "ocr.html",
    },
    {
      "slug": "dococr",
      "label": "Vue OCR Système Complet",
      "data_file": ROOT / "data" / "tools-dococr.json",
      "output": ROOT / "dococr.html",
    },
    {
      "slug": "aicliapps",
      "label": "Vue AI CLI Applications",
      "data_file": ROOT / "data" / "tools-aicliapps.json",
      "output": ROOT / "aicliapps.html",
    },
    {
      "slug": "ia-resources",
      "label": "Ressources IA",
      "data_file": ROOT / "data" / "tools-ia-resources.json",
      "output": ROOT / "ia-resources.html",
      "static": True
    },
]

PAGE_AUDIENCE_GUIDE = {
  "general": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Priorisez les outils avec API claire, documentation maintenue et integration CI/CD avant toute adoption.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Comparez la valeur business, les risques de conformite et le cout total avant de lancer un pilote.",
  },
  "enterprise": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Validez l'architecture, la securite et l'observabilite des stacks IA enterprise en conditions de production.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Cadrez le ROI, la gouvernance des donnees et les exigences de conformite pour un deploiement durable.",
  },
  "discovery": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Utilisez cette page comme radar technologique pour preselectionner des outils testables rapidement.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Identifiez les tendances, puis priorisez les experimentations selon l'impact metier attendu.",
  },
  "ragdev": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Concentrez-vous sur la qualite retrieval, l'evaluation et la stabilite de la pipeline RAG en production.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Suivez les gains de precision, de productivite et de reduction des risques sur les workflows metier.",
  },
  "agentdev": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Evaluez les frameworks d'agents selon la fiabilite, la debuggabilite et la maintenabilite du code.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Selectionnez des solutions agentiques avec trajectoire claire de passage du POC a la production.",
  },
  "vscode": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Choisissez les extensions VS Code qui accelerent revue, refactor et tests sans degrade la qualite.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Encadrez l'usage des extensions IA avec standards d'equipe, securite et mesure de productivite.",
  },
  "newrag": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Explorez les approches RAG de nouvelle generation et comparez leurs compromis techniques.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Reperez les innovations applicables a court terme avec un risque d'integration maitrise.",
  },
  "cowork": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Analysez les integrations techniques pour fluidifier collaboration, documentation et execution equipe.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Suivez l'impact sur coordination transverse, vitesse de livraison et qualite des decisions.",
  },
  "ocr": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Testez precision OCR, extraction structuree et robustesse multi-formats avant industrialisation.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Priorisez les solutions OCR qui reduisent les taches manuelles et les erreurs operationnelles.",
  },
  "dococr": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Validez chaque etape du pipeline documentaire: ingestion, OCR, classification et orchestration.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Pilotez la transformation documentaire avec des KPI de delai, qualite et conformite.",
  },
  "aicliapps": {
    "dev_title": "Pour les developpeurs",
    "dev_text": "Selectionnez des apps CLI IA stables, scriptables et compatibles avec vos workflows d'equipe.",
    "mgr_title": "Pour les managers",
    "mgr_text": "Evaluez l'equilibre entre vitesse d'execution, securite et cout de possession des outils CLI.",
  },
}

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

    /* Light mode */
    html[data-theme="light"] {{
      --bg: #f8f7fc;
      --surface: #ffffff;
      --surface2: #f0edff;
      --border: #e0d9f0;
      --accent: #6c63ff;
      --accent2: #00d4aa;
      --text: #1a1620;
      --muted: #6b6b7d;
      --new: #ff6b6b;
    }}

    html[data-theme="light"] body {{
      background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(108,99,255,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80% 80%, rgba(0,212,170,0.05) 0%, transparent 50%);
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
    .theme-toggle {{
      position: absolute;
      top: 24px;
      right: 24px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      width: 40px;
      height: 40px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      font-size: 18px;
      transition: all 0.2s;
    }}
    .theme-toggle:hover {{
      border-color: var(--accent);
      background: var(--surface);
      transform: scale(1.05);
    }}
    .menu-toggle {{
      position: absolute;
      top: 24px;
      right: 162px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      width: 40px;
      height: 40px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      font-size: 18px;
      transition: all 0.2s;
    }}
    .menu-toggle:hover {{
      border-color: var(--accent2);
      background: var(--surface);
      transform: scale(1.05);
    }}
    .summary-toggle {{
      position: absolute;
      top: 24px;
      right: 116px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      width: 40px;
      height: 40px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      font-size: 18px;
      transition: all 0.2s;
    }}
    .summary-toggle:hover {{
      border-color: var(--accent2);
      background: var(--surface);
      transform: scale(1.05);
    }}
    .panel-toggle {{
      position: absolute;
      top: 24px;
      right: 70px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      width: 40px;
      height: 40px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      font-size: 18px;
      transition: all 0.2s;
    }}
    .panel-toggle:hover {{
      border-color: var(--accent2);
      background: var(--surface);
      transform: scale(1.05);
    }}
    .layout-columns-toggle {{
      position: absolute;
      top: 24px;
      right: 208px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      width: 40px;
      height: 40px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--text);
      font-size: 18px;
      transition: all 0.2s;
    }}
    .layout-columns-toggle:hover {{
      border-color: var(--accent2);
      background: var(--surface);
      transform: scale(1.05);
    }}
    button[aria-pressed="false"] {{
      opacity: 0.5;
      filter: brightness(0.7);
    }}
    button[aria-pressed="false"]:hover {{
      opacity: 0.8;
      filter: brightness(0.85);
    }}
    .current-page-label {{
      position: absolute;
      top: 24px;
      right: 254px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 8px 12px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      color: var(--accent2);
      letter-spacing: 0.06em;
      text-transform: uppercase;
      text-align: center;
      min-width: 60px;
      transition: all 0.2s;
    }}
    .current-page-label.hidden {{
      display: none;
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
      background: linear-gradient(135deg, var(--text) 30%, var(--accent));
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
    .header-summary.hidden {{
      display: none;
    }}
    .page-switcher {{
      margin-top: 20px;
      display: inline-flex;
      gap: 8px;
      flex-wrap: wrap;
      justify-content: center;
      padding: 8px;
      border-radius: 999px;
      border: 1px solid var(--border);
      background: var(--surface);
    }}
    .page-switcher.hidden {{
      display: none;
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
    .page-link-static {{
      text-decoration: none;
      color: var(--muted);
      font-size: 12px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 999px;
      border: 1px solid transparent;
      transition: all 0.2s;
    }}
    .page-link-static.active, .page-link-static:hover {{
      color: #fff;
      border-color: var(--accent2);
      background: var(--accent2);
    }}
    .page-meta {{
      margin: 20px auto 0;
      max-width: 820px;
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 12px;
      align-items: center;
      padding: 14px 16px;
      transition: all 0.3s ease;
    }}
    .page-meta.hidden {{
      display: none;
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
    .audience-brief {{
      margin: 18px auto 0;
      max-width: 980px;
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      transition: all 0.3s ease;
    }}
    .audience-brief.hidden {{
      display: none;
    }}
    .reader-card {{
      border: 1px solid var(--border);
      border-radius: var(--radius);
      background: var(--surface);
      padding: 14px 16px;
      text-align: left;
    }}
    .reader-label {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--accent2);
      margin-bottom: 6px;
    }}
    .reader-title {{
      font-size: 15px;
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .reader-text {{
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
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
    nav.hidden {{
      display: none;
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
    body[data-grid-columns="1"] .tools-grid {{
      grid-template-columns: repeat(1, minmax(0, 1fr));
    }}
    body[data-grid-columns="2"] .tools-grid {{
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
    body[data-grid-columns="3"] .tools-grid {{
      grid-template-columns: repeat(3, minmax(0, 1fr));
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
      body[data-grid-columns="1"] .tools-grid {{ grid-template-columns: 1fr; }}
      body[data-grid-columns="2"] .tools-grid {{ grid-template-columns: 1fr 1fr; }}
      body[data-grid-columns="3"] .tools-grid {{ grid-template-columns: 1fr 1fr; }}
      .page-meta {{ grid-template-columns: 1fr; }}
      .audience-brief {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>

<header>
  <div class="current-page-label" id="current-page-label">{page_slug}</div>
  <button class="menu-toggle" id="menu-toggle" aria-label="Masquer le menu" aria-pressed="true" title="Masquer le menu">🧭</button>
  <button class="summary-toggle" id="summary-toggle" aria-label="Masquer les infos d'en-tete" aria-pressed="true" title="Masquer les infos d'en-tete">ℹ️</button>
  <button class="panel-toggle" id="panel-toggle" aria-label="Afficher/Masquer les panneaux" aria-pressed="true" title="Afficher/Masquer les panneaux">📋</button>
  <button class="layout-columns-toggle" id="layout-columns-toggle" aria-label="Changer le nombre de colonnes" aria-pressed="true" title="Changer le nombre de colonnes">⊞</button>
  <button class="theme-toggle" id="theme-toggle" aria-label="Activer le mode clair" aria-pressed="false" title="Activer le mode clair">🌙</button>
  <div class="header-badge">🤖 Auto-updated by AI · {today}</div>
  <h1>{title}</h1>
  <div class="header-summary" id="header-summary">
    <p class="subtitle">{subtitle}</p>
    <p class="update-info">Dernière mise à jour : <span>{last_updated}</span></p>
    <p class="update-info">Outils : <span>{tool_count}</span> · Nouveaux : <span>{new_tool_count}</span></p>
  </div>
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
      <button class="info-btn" type="button" id="export-page-zip">ZIP Page</button>
      <button class="info-btn" type="button" id="export-all-zip">ZIP All</button>
    </div>
  </div>
  <div class="audience-brief">
    <article class="reader-card reader-dev">
      <div class="reader-label">Public cible</div>
      <div class="reader-title">{dev_reader_title}</div>
      <div class="reader-text">{dev_reader_text}</div>
    </article>
    <article class="reader-card reader-manager">
      <div class="reader-label">Public cible</div>
      <div class="reader-title">{manager_reader_title}</div>
      <div class="reader-text">{manager_reader_text}</div>
    </article>
  </div>
</header>

<nav id="category-nav">
  <a class="nav-tab active" href="#" data-cat="all">Tout voir</a>
  {nav_tabs}
</nav>

<main>
  {categories_html}
</main>

<footer>
  Généré automatiquement par GitHub Actions + Gemini AI ·
  Copyright made by joffroy ·
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
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {history_html}
      </tbody>
    </table>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js"></script>
<script>
  const tabs = document.querySelectorAll('.nav-tab');
  const categories = document.querySelectorAll('.category');
  const searchModal = document.getElementById('search-modal');
  const historyModal = document.getElementById('history-modal');
  const openSearchInfo = document.getElementById('open-search-info');
  const closeSearchInfo = document.getElementById('close-search-info');
  const openHistoryInfo = document.getElementById('open-history-info');
  const closeHistoryInfo = document.getElementById('close-history-info');
  const exportPageZipBtn = document.getElementById('export-page-zip');
  const exportAllZipBtn = document.getElementById('export-all-zip');
  const layoutColumnsToggle = document.getElementById('layout-columns-toggle');
  const currentPageLabel = document.getElementById('current-page-label');
  const currentPageFile = '{history_page_file}';
  const exportManifest = {export_manifest_json};
  const menuToggle = document.getElementById('menu-toggle');
  const pageSwitcher = document.querySelector('.page-switcher');
  const categoryNav = document.getElementById('category-nav');
  const summaryToggle = document.getElementById('summary-toggle');
  const headerSummary = document.getElementById('header-summary');
  const panelToggle = document.getElementById('panel-toggle');
  const pageMeta = document.querySelector('.page-meta');
  const audienceBrief = document.querySelector('.audience-brief');

  async function fetchAsText(path) {{
    const res = await fetch(path, {{ cache: 'no-store' }});
    if (!res.ok) throw new Error(`Failed to fetch ${{path}} (${{res.status}})`);
    return res.text();
  }}

  function downloadBlob(filename, blob) {{
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }}

  async function exportZip(files, zipName) {{
    const zip = new JSZip();
    for (const item of files) {{
      const content = await fetchAsText(item.path);
      zip.file(item.name, content);
    }}
    const blob = await zip.generateAsync({{ type: 'blob' }});
    downloadBlob(zipName, blob);
  }}

  exportPageZipBtn.addEventListener('click', async () => {{
    const current = exportManifest.pages.find(p => p.html === currentPageFile);
    if (!current) return;
    try {{
      await exportZip([
        {{ path: current.html, name: current.html }},
        {{ path: current.data, name: current.data }},
      ], `export-${{current.slug}}.zip`);
    }} catch (err) {{
      alert(`Export page failed: ${{err.message}}`);
    }}
  }});

  exportAllZipBtn.addEventListener('click', async () => {{
    try {{
      const files = [];
      for (const p of exportManifest.pages) {{
        files.push({{ path: p.html, name: p.html }});
        files.push({{ path: p.data, name: p.data }});
      }}
      await exportZip(files, 'export-all-pages.zip');
    }} catch (err) {{
      alert(`Export all failed: ${{err.message}}`);
    }}
  }});

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

  // Theme toggle functionality
  const themeToggle = document.getElementById('theme-toggle');
  const htmlElement = document.documentElement;
  const storedTheme = localStorage.getItem('theme') || 'dark';

  // Set initial theme
  htmlElement.setAttribute('data-theme', storedTheme);
  updateThemeToggle();

  function updateThemeToggle() {{
    const currentTheme = htmlElement.getAttribute('data-theme');
    const isDark = currentTheme === 'dark';
    themeToggle.textContent = isDark ? '☀️' : '🌙';
    themeToggle.setAttribute('aria-pressed', String(!isDark));
    themeToggle.setAttribute('aria-label', isDark ? 'Activer le mode clair' : 'Activer le mode sombre');
    themeToggle.setAttribute('title', isDark ? 'Activer le mode clair' : 'Activer le mode sombre');
  }}

  themeToggle.addEventListener('click', () => {{
    const currentTheme = htmlElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    htmlElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeToggle();
  }});

  // Layout columns toggle button (cycles through: 1 -> now -> 2 -> 3 -> 1)
  const validGridLayouts = ['1', 'now', '2', '3'];
  const storedGridColumns = localStorage.getItem('gridColumnsLayout') || 'now';

  function applyGridColumnsLayout(layoutValue) {{
    if (layoutValue === 'now') {{
      document.body.removeAttribute('data-grid-columns');
      return;
    }}
    document.body.setAttribute('data-grid-columns', layoutValue);
  }}

  function updateLayoutToggle() {{
    const currentLayout = localStorage.getItem('gridColumnsLayout') || 'now';
    const isDefault = currentLayout === 'now';
    layoutColumnsToggle.setAttribute('aria-pressed', String(isDefault));
    layoutColumnsToggle.setAttribute('title', `Colonnes: ${{currentLayout}}`);
    updateAllButtonStates();
  }}

  function cycleLayoutColumns() {{
    const currentLayout = localStorage.getItem('gridColumnsLayout') || 'now';
    const currentIndex = validGridLayouts.indexOf(currentLayout);
    const nextIndex = (currentIndex + 1) % validGridLayouts.length;
    const nextLayout = validGridLayouts[nextIndex];
    applyGridColumnsLayout(nextLayout);
    localStorage.setItem('gridColumnsLayout', nextLayout);
    updateLayoutToggle();
  }}

  const initialGridLayout = validGridLayouts.includes(storedGridColumns) ? storedGridColumns : 'now';
  applyGridColumnsLayout(initialGridLayout);
  updateLayoutToggle();

  layoutColumnsToggle.addEventListener('click', cycleLayoutColumns);

  // Menu toggle (page switcher + category nav)
  const storedMenuState = localStorage.getItem('menuVisible');
  const menuVisible = storedMenuState === null ? true : storedMenuState === 'true';

  function updateMenuToggle() {{
    const isVisible = !pageSwitcher.classList.contains('hidden') && !categoryNav.classList.contains('hidden');
    menuToggle.setAttribute('aria-pressed', String(isVisible));
    menuToggle.setAttribute('aria-label', isVisible ? 'Masquer le menu' : 'Afficher le menu');
    menuToggle.setAttribute('title', isVisible ? 'Masquer le menu' : 'Afficher le menu');
    updateAllButtonStates();
  }}

  function toggleMenu() {{
    const isHidden = pageSwitcher.classList.contains('hidden') || categoryNav.classList.contains('hidden');
    if (isHidden) {{
      pageSwitcher.classList.remove('hidden');
      categoryNav.classList.remove('hidden');
      localStorage.setItem('menuVisible', 'true');
    }} else {{
      pageSwitcher.classList.add('hidden');
      categoryNav.classList.add('hidden');
      localStorage.setItem('menuVisible', 'false');
    }}
    updateMenuToggle();
  }}

  if (!menuVisible) {{
    pageSwitcher.classList.add('hidden');
    categoryNav.classList.add('hidden');
  }}
  updateMenuToggle();
  menuToggle.addEventListener('click', toggleMenu);

  // Header summary toggle (subtitle + stats)
  const storedSummaryState = localStorage.getItem('headerSummaryVisible');
  const summaryVisible = storedSummaryState === null ? true : storedSummaryState === 'true';

  function updateSummaryToggle() {{
    const isVisible = !headerSummary.classList.contains('hidden');
    summaryToggle.setAttribute('aria-pressed', String(isVisible));
    summaryToggle.setAttribute('aria-label', isVisible ? "Masquer les infos d'en-tete" : "Afficher les infos d'en-tete");
    summaryToggle.setAttribute('title', isVisible ? "Masquer les infos d'en-tete" : "Afficher les infos d'en-tete");
    updateAllButtonStates();
  }}

  function toggleHeaderSummary() {{
    const isHidden = headerSummary.classList.contains('hidden');
    if (isHidden) {{
      headerSummary.classList.remove('hidden');
      localStorage.setItem('headerSummaryVisible', 'true');
    }} else {{
      headerSummary.classList.add('hidden');
      localStorage.setItem('headerSummaryVisible', 'false');
    }}
    updateSummaryToggle();
  }}

  if (!summaryVisible) {{
    headerSummary.classList.add('hidden');
  }}
  updateSummaryToggle();
  summaryToggle.addEventListener('click', toggleHeaderSummary);

  // Panel toggle functionality
  const storedPanelState = localStorage.getItem('panelsVisible');
  const panelsVisible = storedPanelState === null ? true : storedPanelState === 'true';

  function updatePanelToggle() {{
    const isVisible = !pageMeta.classList.contains('hidden');
    panelToggle.setAttribute('aria-pressed', String(isVisible));
    panelToggle.setAttribute('aria-label', isVisible ? 'Masquer les panneaux' : 'Afficher les panneaux');
    panelToggle.setAttribute('title', isVisible ? 'Masquer les panneaux' : 'Afficher les panneaux');
    updateAllButtonStates();
  }}

  function togglePanels() {{
    const isHidden = pageMeta.classList.contains('hidden');
    if (isHidden) {{
      pageMeta.classList.remove('hidden');
      audienceBrief.classList.remove('hidden');
      localStorage.setItem('panelsVisible', 'true');
    }} else {{
      pageMeta.classList.add('hidden');
      audienceBrief.classList.add('hidden');
      localStorage.setItem('panelsVisible', 'false');
    }}
    updatePanelToggle();
  }}

  // Initialize panel state
  if (!panelsVisible) {{
    pageMeta.classList.add('hidden');
    audienceBrief.classList.add('hidden');
  }}
  updatePanelToggle();

  panelToggle.addEventListener('click', togglePanels);

  // Master function to sync all button aria-pressed states and page label visibility
  function updateAllButtonStates() {{
    // Update page label visibility: show when menu is hidden, hide when menu is visible
    const isMenuVisible = !pageSwitcher.classList.contains('hidden');
    if (isMenuVisible) {{
      currentPageLabel.classList.add('hidden');
    }} else {{
      currentPageLabel.classList.remove('hidden');
    }}
  }}

  // Initialize all button states
  updateAllButtonStates();
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
        base_style = "page-link"
        href = cfg["output"].name

        if cfg.get("static"):
            base_style = "page-link-static"
        classes = base_style + (" active" if cfg["slug"] == active_slug else "")
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


def count_new_tools(categories: list[dict]) -> int:
    """Count tools marked as new across all categories and subcategories."""
    total = 0
    for cat in categories:
        for sub in cat.get("subcategories", []):
            for tool in sub.get("tools", []):
                if tool.get("new"):
                    total += 1
    return total


def render_history(page_history: list[dict], current_page_file: str) -> str:
    """Render history table rows."""
    if not page_history:
        return "<tr><td colspan='3' style='text-align: center; color: var(--muted);'>Aucun historique disponible</td></tr>"

    rows = []
    for entry in page_history:
        date_str = entry.get("generated_at") or entry.get("date", "?")
        tool_count = entry.get("tool_count", 0)
        snapshot_file = entry.get("snapshot_file")

        if snapshot_file:
            date_cell = f'<a href="{escape(snapshot_file)}" target="_blank">{escape(str(date_str))}</a>'
            compare_url = "compare-view.html?left=" + quote(snapshot_file) + "&right=" + quote(current_page_file)
            actions = (
                f'<a href="{escape(snapshot_file)}" target="_blank">Voir</a> · '
                f'<a href="{escape(compare_url)}">Comparer</a>'
            )
        else:
            date_cell = escape(str(date_str))
            actions = "-"

        rows.append(f"""        <tr>
          <td class="history-date">{date_cell}</td>
          <td class="history-count">{tool_count}</td>
          <td>{actions}</td>
        </tr>""")
    return "\n".join(rows)


def build_export_manifest() -> str:
    pages = []
    for cfg in PAGE_CONFIGS:
        pages.append(
            {
                "slug": cfg["slug"],
                "html": cfg["output"].name,
                "data": cfg["data_file"].relative_to(ROOT).as_posix(),
            }
        )
    return json.dumps({"pages": pages}, ensure_ascii=False)


def load_search_query_map() -> dict[str, list[str]]:
    queries_file = ROOT / "data" / "search_queries.json"
    if not queries_file.exists():
        return {}
    with open(queries_file, "r", encoding="utf-8") as f:
        payload = json.load(f)
    profiles = payload.get("profiles", {})

    query_map: dict[str, list[str]] = {}
    for slug, block in profiles.items():
        queries = block.get("queries", []) if isinstance(block, dict) else []
        query_map[slug] = [q.strip() for q in queries if isinstance(q, str) and q.strip()]
    return query_map


def generate_compare_view_page():
    compare_html = """<!DOCTYPE html>
<html lang=\"fr\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Comparaison des versions</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; background: #0f1116; color: #f2f4f8; }
    header { padding: 12px 16px; border-bottom: 1px solid #2d3440; display: flex; gap: 12px; align-items: center; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; height: calc(100vh - 58px); padding: 8px; }
    iframe { width: 100%; height: 100%; border: 1px solid #2d3440; background: #fff; }
    a { color: #5cc8ff; }
    @media (max-width: 900px) { .grid { grid-template-columns: 1fr; height: auto; } iframe { min-height: 60vh; } }
  </style>
</head>
<body>
  <header>
    <strong>Comparaison</strong>
    <a href=\"javascript:history.back()\">Retour</a>
    <span id=\"meta\"></span>
  </header>
  <div class=\"grid\">
    <iframe id=\"left\" title=\"Version historique\"></iframe>
    <iframe id=\"right\" title=\"Version actuelle\"></iframe>
  </div>
  <script>
    const params = new URLSearchParams(window.location.search);
    const left = params.get('left');
    const right = params.get('right');
    if (left) document.getElementById('left').src = left;
    if (right) document.getElementById('right').src = right;
    document.getElementById('meta').textContent = `Historique: ${left || '-'} | Actuelle: ${right || '-'}`;
  </script>
</body>
</html>"""
    (ROOT / "compare-view.html").write_text(compare_html, encoding="utf-8")


def generate_page(page_cfg: dict, search_query_map: dict[str, list[str]]):
    data_file = page_cfg["data_file"]
    output_file = page_cfg["output"]
    if not data_file.exists():
        print(f"Skipping {output_file.name}: missing {data_file.name}")
        return

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    meta = data["meta"]
    cats = data["categories"]

    # Count tools and manage history per run.
    tool_count = count_tools(cats)
    new_tool_count = count_new_tools(cats)
    now_iso = datetime.now().isoformat(timespec="milliseconds").replace("T", " ")
    snapshot_name = now_iso.replace(" ", "_").replace(":", "-").replace(".", "-") + ".html"
    snapshot_dir = ROOT / "snapshots" / page_cfg["slug"]
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / snapshot_name
    snapshot_rel = snapshot_path.relative_to(ROOT).as_posix()

    # Load existing history and add new entry.
    page_history = meta.get("page_history", [])
    new_entry = {
        "generated_at": now_iso,
        "tool_count": tool_count,
      "snapshot_file": snapshot_rel,
    }
    page_history.append(new_entry)

    # Keep only last 10 entries.
    page_history = page_history[-10:]

    # Keep snapshots aligned with retained history to avoid unbounded growth.
    allowed_snapshot_names = {
      Path(entry["snapshot_file"]).name
      for entry in page_history
      if isinstance(entry, dict) and entry.get("snapshot_file")
    }
    for existing_snapshot in snapshot_dir.glob("*.html"):
      if existing_snapshot.name not in allowed_snapshot_names:
        existing_snapshot.unlink(missing_ok=True)

    # Update meta with new history.
    meta["page_history"] = page_history

    # Save updated data file.
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
    page_name = meta.get("page_name", page_cfg["slug"])
    authoritative_queries = search_query_map.get(page_name, meta.get("search_queries", []))
    meta["search_queries"] = authoritative_queries
    audience = PAGE_AUDIENCE_GUIDE.get(meta.get("page_name", "general"), PAGE_AUDIENCE_GUIDE["general"])
    search_queries_html = render_search_queries(authoritative_queries)
    history_html = render_history(page_history, output_file.name)

    repo_name = "joffroy59/IA_survey"  # remplacer

    html = HTML_TEMPLATE.format(
        title=meta["title"],
        subtitle=meta["subtitle"],
        today=date.today().strftime("%d/%m/%Y"),
        last_updated=meta.get("last_updated", ""),
        tool_count=tool_count,
        new_tool_count=new_tool_count,
        history_page_file=output_file.name,
        export_manifest_json=build_export_manifest(),
        page_slug=escape(page_cfg["slug"]),
        page_switcher=render_page_switcher(meta.get("page_name", "general")),
        page_label=escape(page_label),
        page_description=escape(page_description),
        dev_reader_title=escape(audience["dev_title"]),
        dev_reader_text=escape(audience["dev_text"]),
        manager_reader_title=escape(audience["mgr_title"]),
        manager_reader_text=escape(audience["mgr_text"]),
        search_queries_html=search_queries_html,
        history_html=history_html,
        nav_tabs=nav_tabs,
        categories_html=categories_html,
        repo_name=repo_name,
    )

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    # Save immutable snapshot for history view/compare.
    with open(snapshot_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ {output_file.name} generated ({output_file})")


def generate():
    search_query_map = load_search_query_map()
    generate_compare_view_page()
    for page_cfg in PAGE_CONFIGS:
        generate_page(page_cfg, search_query_map)


if __name__ == "__main__":
    generate()
