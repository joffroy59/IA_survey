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
git clone https://joffroy59.github.io/IA_survey/
```

### 2. Configurer un provider LLM

Provider par défaut: **Gemini**.

Option A (Gemini):
- [aistudio.google.com](https://aistudio.google.com) → **Get API Key**
- Utiliser la variable `GEMINI_API_KEY`

Option B (autres providers):
- OpenAI: `OPENAI_API_KEY`
- OpenRouter: `OPENROUTER_API_KEY`
- Ollama: local (`http://localhost:11434/v1`)
- LM Studio: local (`http://localhost:1234/v1`)

### 3. Ajouter les secrets GitHub nécessaires

```
Settings → Secrets and variables → Actions → New repository secret
Name  : GEMINI_API_KEY
Value : votre-clé-ici
```

Si vous utilisez OpenAI ou OpenRouter, ajoutez aussi:

```
OPENAI_API_KEY
OPENROUTER_API_KEY
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

## Global Settings Panel (providers)

Le fichier global est `data/global_settings.json`.

Commandes utiles:

```bash
# Ouvrir le panneau global (CLI interactif)
python scripts/update.py --settings-panel

# Définir le provider par défaut
python scripts/update.py --set-provider openrouter

# Override provider uniquement pour ce run
python scripts/update.py --provider ollama --profile general --dry-run
```
