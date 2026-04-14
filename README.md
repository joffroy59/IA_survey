# 🤖 AI Toolbox — Auto-updated

Boîte à outils IA mise à jour automatiquement chaque semaine par GitHub Actions + Gemini AI.

🔗 **[Voir la page en direct](https://joffroy59.github.io/IA_survey/)**

## Stack (100% gratuit)

| Composant | Outil | Limite gratuite |
|-----------|-------|-----------------|
| LLM | Google Gemini Flash | 1 500 req/jour |
| Search | DuckDuckGo | Illimité |
| CI/CD | GitHub Actions | 2 000 min/mois |
| Hosting | GitHub Pages | Illimité |

## Setup (5 minutes)

### 1. Fork ce dépôt

```bash
git clone https://github.com/VOTRE-USERNAME/ai-toolbox
```

### 2. Obtenir une clé Gemini gratuite

→ [aistudio.google.com](https://aistudio.google.com) → **Get API Key** → Copier la clé

### 3. Ajouter le secret GitHub

```
Settings → Secrets and variables → Actions → New repository secret
Name  : GEMINI_API_KEY
Value : votre-clé-ici
```

### 4. Activer GitHub Pages

```
Settings → Pages → Source : Deploy from a branch → Branch: main / root
```

### 5. Premier run

```
Actions → "Update AI Toolbox" → Run workflow
```

## Structure

```
├── .github/workflows/update.yml   # Cron hebdomadaire
├── data/tools.json                 # Source de vérité
├── scripts/
│   ├── update.py                   # Search + Gemini → tools.json
│   └── generate.py                 # tools.json → index.html
├── index.html                      # Page générée (auto)
└── requirements.txt
```

## Personnalisation

- **Ajouter un outil manuellement** : éditer `data/tools.json`
- **Changer la fréquence** : modifier le cron dans `.github/workflows/update.yml`
- **Changer le style** : modifier le `HTML_TEMPLATE` dans `scripts/generate.py`
