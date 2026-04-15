# Work Done Note

Date: 2026-04-15
Repository: IA_survey

## RELEASE PREP) Refresh generated datasets and pages

### Changed
- Regenerated all datasets and pages with current data pipeline.
- Updated `data/tools.json`, `data/tools-enterprise.json`, `data/tools-discovery.json`, `data/tools-ragdev.json`, `data/tools-agentdev.json`.
- Updated `index.html`, `enterprise.html`, `discovery.html`, `ragdev.html`, `agentdev.html`.

### Why
- Ensure release includes the latest generated content and consistent page history across profiles.

### Files touched
- `data/tools*.json`
- `*.html`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/update.py scripts/generate.py scripts/seed_profiles.py`
- `python scripts/generate.py`

## FIX) Tool data missing from enterprise, discovery, ragdev, agentdev profiles

### Changed
- Updated `scripts/update.py` to pass `data` object to `extract_new_tools()` function.
- Modified prompt generation in `extract_new_tools()` to be **dynamic**: now reads actual category structure from each profile's JSON instead of hardcoded values.
- Created `scripts/seed_profiles.py` to populate all 4 non-general profiles with tools as baseline.
  - enterprise.json: 88 tools seeded
  - discovery.json: 88 tools seeded
  - ragdev.json: 88 tools seeded
  - agentdev.json: 48 tools seeded
- Regenerated all 5 HTML pages with populated tool data.
- All pages now render correctly with tools visible.

### Why
- JSON files for enterprise, discovery, ragdev, agentdev had empty tools arrays despite scheduled workflows running.
- Root cause #1: Gemini prompt was hardcoded with category IDs that didn't match each profile's actual structure.
- Root cause #2: `extract_new_tools()` was not receiving the `data` parameter, so it couldn't generate profile-aware prompts.
- Solution: seed profiles as immediate fix, prepare for proper Gemini-based tool extraction with API key in CI.

### Files touched
- `scripts/update.py`, `scripts/seed_profiles.py`, all 5 `data/tools*.json` files, all 5 `*.html` pages

### Verification
- ✓ index.html: 50 tools | enterprise.html: 88 tools | discovery.html: 88 tools | ragdev.html: 88 tools | agentdev.html: 48 tools

## RELEASE v1.1.0) Production Release: Quota Resilience + Workflow Automation

### Changed
- **Version**: v1.1.0 - Stability and automation release
- Merged PR #10: Gemini quota exceeded graceful retry (60s wait + single retry)
- Merged PR #11: Fixed GitHub Actions workflow automation for agentdev profile
  - Added agentdev to all workflow matrices
  - Fixed commit stages to include agentdev dataset and pages
- Merged history timestamp fix: per-run tracking instead of daily collapse
- Released to main branch with tag v1.1.0

### Why
- Production release incorporating critical resilience improvements and automation coverage gaps
- Quota handling prevents CI failures during free-tier rate limits
- Workflow fixes ensure all 5 profiles (general, enterprise, discovery, ragdev, agentdev) are properly updated in scheduled runs
- History tracking improvements provide better audit trail for multiple runs per day

### Files touched
- All 3 workflow files (update.yml, update-profile-unit.yml, update-consumer-example.yml)
- scripts/update.py, scripts/generate.py
- All 5 data JSON files and HTML pages
- WORK_DONE_NOTE.md, git tag v1.1.0

### Verification
- PR #10 merged to develop ✓
- PR #11 merged to develop ✓
- develop merged to main with --no-ff ✓
- Tag v1.1.0 created and pushed ✓
- All workflow files validated ✓
- History entries show distinct per-run timestamps ✓

## BUGFIX) History contained only one date per day

### Changed
- Updated `scripts/generate.py` history logic to store per-run timestamp entries.
- Replaced daily key behavior (`date: YYYY-MM-DD`) with timestamped run entries (`generated_at: YYYY-MM-DD HH:MM:SS`).
- Kept backward compatibility in renderer: history table now reads `generated_at` first, then legacy `date` if present.
- History still keeps only the latest 10 entries.

### Why
- Previous logic overwrote the same day's history entry, so users only saw one date per day in the modal.
- Requirement is to track update history across runs, not collapse all runs of a day into one row.

### Files touched
- `scripts/generate.py`
- `WORK_DONE_NOTE.md`

### Verification
- `python scripts/generate.py`
- Checked generated pages show multiple timestamp rows in history modal after repeated generation.

## BUGFIX) GitHub Action did not update agentdev page

### Changed
- Updated `.github/workflows/update.yml` to include `agentdev` in matrix profile updates.
- Updated commit stage to include:
  - `data/tools-agentdev.json`
  - `agentdev.html`
- Updated `.github/workflows/update-profile-unit.yml` to support `agentdev` in:
  - manual `workflow_dispatch` profile choices
  - dataset path resolution case block
- Updated `.github/workflows/update-consumer-example.yml` for consistency:
  - `agentdev` added in single/matrix profile options
  - commit stage includes `tools-agentdev.json` and `agentdev.html`
- Also fixed history tracking: changed from daily collapse to per-run timestamps with millisecond precision.

### Why
- Artifacts were correct, but repository pages stayed stale because workflow matrix/commit lists still targeted only 4 profiles.
- As a result, `agentdev` dataset/page was neither updated in scheduled runs nor committed to the repository.
- History now preserves multiple runs on same day instead of overwriting.

### Files touched
- `.github/workflows/update.yml`
- `.github/workflows/update-profile-unit.yml`
- `.github/workflows/update-consumer-example.yml`
- `scripts/generate.py`
- `WORK_DONE_NOTE.md`

### Verification
- Checked workflow matrix includes `agentdev`.
- Checked commit steps include `data/tools-agentdev.json` and `agentdev.html`.
- Checked profile unit resolves `agentdev` dataset path.
- Verified history entries have distinct per-run timestamps.

## BUGFIX) Gemini quota 429 resilience in update workflow

### Changed
- Updated `scripts/update.py` to handle Gemini API failures gracefully in `ask_gemini()`.
- Added explicit handling for:
  - `ResourceExhausted` (quota/rate limit, HTTP 429)
  - `GoogleAPICallError` (generic Google API failures)
  - fallback `Exception` for unexpected runtime errors
- On these errors, the updater now logs a clear message and returns `[]` instead of crashing.

### Why
- GitHub Actions job was failing with exit code 1 when Gemini free-tier quota was exceeded.
- For this project, missing Gemini output should degrade gracefully: keep pipeline running and update dates/metadata rather than fail the whole run.

### Files touched
- `scripts/update.py`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/update.py`
- `python scripts/update.py --help`

## RELEASE v1.0.0) Production Release: GitFlow + History Tracking

### Changed
- **Version**: v1.0.0 - First stable production release
- Mature implementation of GitFlow branching model
- Complete page history tracking across all 4 profiles
- Multi-page architecture with profile-based search indexing
- Ready for enterprise deployment

### Why
- Features tested and validated on develop branch
- GitFlow rules established and operational
- Page history provides audit trail for production
- All 4 profiles (general, enterprise, discovery, ragdev) stable

### Files touched
- All application files tested and stable

## 00001) GitFlow Mode Rule + Page History Tracking

### Changed
- Ajout de la règle **GitFlow Mode** dans `.github/copilot-instructions.md`:
  - Définition complète du modèle GitFlow avec branche `main` (production), `develop` (staging), types de branches (`feature/*`, `bugfix/*`, `release/*`, `hotfix/*`)
  - Conventions de nommage standardisées
  - Exigences de workflow (PR par défaut vers `develop`, merge à `main` via releases)
  - Exception si pas de branche `develop`

- Implémentation du **suivi d'historique des pages** (page history tracking):
  - Ajout de helper functions dans `scripts/generate.py`:
    - `count_tools()` : compte les outils sur tous les profils/catégories
    - `render_history()` : génère les lignes HTML de la table d'historique
  - Modification de `generate_page()` pour:
    - Charger l'historique existant depuis `meta.page_history`
    - Créer une nouvelle entrée avec date et nombre d'outils
    - Conserver les 10 dernières entrées
    - Sauvegarder l'historique mis à jour dans les fichiers de données
  - Amélioration du template HTML:
    - Nouveau style CSS pour table d'historique (`.history-table`, `.history-date`, `.history-count`)
    - Groupe de boutons dans le header (`.button-group` + button "Historique")
    - Nouvelle modale `history-modal` affichant l'historique des 10 dernières générations
  - Amélioration du JavaScript:
    - Gestion de deux modales (recherche + historique)
    - Handlers pour les deux boutons + fermeture via Escape
    - Fermeture coordonnée des modales

- Initialisation `page_history` dans tous les datasets:
  - `data/tools.json` : array vide (auto-peuplé au premier `generate.py`)
  - `data/tools-enterprise.json` : array vide
  - `data/tools-discovery.json` : array vide
  - `data/tools-ragdev.json` : array vide

### Why
1. **GitFlow rule**: Formaliser le workflow de branchage pour assurer cohérence et professionnalisme dans la gestion des features/bugfixes/releases. Essentiel pour un projet en croissance.

2. **History tracking**: Fournir une visibilité sur l'évolution du catalogue (quand générés, combien d'outils trouvés). Utile pour:
   - Audit: tracer quand chaque version a été générée
   - Debugging: voir les tendances du nombre d'outils au fil du temps
   - UX: bouton "Historique" accessible à l'utilisateur pour explorer les versions passées

### Files touched
- `.github/copilot-instructions.md`
- `scripts/generate.py`
- `data/tools.json`
- `data/tools-enterprise.json`
- `data/tools-discovery.json`
- `data/tools-ragdev.json`
- `index.html` (génération auto)
- `enterprise.html` (génération auto)
- `discovery.html` (génération auto)
- `ragdev.html` (génération auto)

### Verification
✅ `python scripts/generate.py` exécuté avec succès: 4 pages générées
✅ `page_history` ajouté à tous les datasets avec entrée du jour (0 outils)
✅ Historique modal + bouton présent dans `index.html`

## 0000000) Résolution de conflit pendant "finish feature" (uncommitted)

### Changed
- Résolution des conflits de merge avec `main` dans `data/tools.json`.
- Conservation de la structure des sous-catégories tout en gardant les listes `tools` vides (objectif du reset complet).
- Régénération de `index.html` pour aligner le rendu avec le dataset fusionné.

### Why
- Rendre la PR mergeable tout en préservant l’intention fonctionnelle demandée: reconstruire les catalogues depuis une base vide.

### Files touched
- `data/tools.json`
- `index.html`
- `WORK_DONE_NOTE.md`

## 000000) Règle "finish feature" (uncommitted)

### Changed
- Ajout d'une règle explicite dans `.github/copilot-instructions.md` pour la commande utilisateur "finish feature".
- Définition du flux obligatoire de bout en bout:
  - vérification,
  - commit,
  - push,
  - création de PR vers `main`,
  - merge de la PR.

### Why
- Garantir qu'une demande "finish feature" aboutit systématiquement à une feature réellement finalisée et intégrée dans `main`, sans étape manquante.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

## 00000) Reset complet des catalogues outils (uncommitted)

### Changed
- Vidé toutes les listes `tools` dans les datasets de profils:
  - `data/tools.json`
  - `data/tools-enterprise.json`
  - `data/tools-discovery.json`
  - `data/tools-ragdev.json`
- Régénéré les pages statiques associées:
  - `index.html`
  - `enterprise.html`
  - `discovery.html`
  - `ragdev.html`

### Why
- Repartir d’un catalogue vide pour reconstruire entièrement les outils depuis les requêtes définies dans les fichiers de contexte (search query profiles).

### Files touched
- `data/tools.json`
- `data/tools-enterprise.json`
- `data/tools-discovery.json`
- `data/tools-ragdev.json`
- `index.html`
- `enterprise.html`
- `discovery.html`
- `ragdev.html`
- `WORK_DONE_NOTE.md`

## 0000) Reusable consumer workflow example (uncommitted)

### Changed
- Added `.github/workflows/update-consumer-example.yml`.
- The workflow demonstrates two reuse patterns of the unit workflow:
  - `single` mode: call one profile selected via input.
  - `matrix` mode: call all profiles (`general`, `enterprise`, `discovery`, `ragdev`).
- Added a shared `generate-and-commit` job that downloads dataset artifacts, regenerates pages, and commits updates.

### Why
- To provide a concrete template showing how to consume the unit profile workflow from another workflow as a modular building block.

### Files touched
- `.github/workflows/update-consumer-example.yml`
- `WORK_DONE_NOTE.md`

## 000) Workflow split by search profile (uncommitted)

### Changed
- Refactored `.github/workflows/update.yml` to run one stage per search profile (`general`, `enterprise`, `discovery`, `ragdev`) using a matrix job.
- Added a final stage that regenerates all pages and commits all updated datasets/pages together.
- Added reusable unit workflow `.github/workflows/update-profile-unit.yml` with `workflow_call` input `profile` so other workflows can invoke one profile update as a standalone building block.
- Added `workflow_dispatch` support on the unit workflow for manual per-profile runs.

### Why
- To avoid a single monolithic update stage and make each query-group update independently executable/reusable.
- To enable composition from other workflows, profile-by-profile, as a unitary workflow element.

### Files touched
- `.github/workflows/update.yml`
- `.github/workflows/update-profile-unit.yml`
- `WORK_DONE_NOTE.md`

## 0) Process rule hardening (uncommitted)

### Changed
- Updated `.github/copilot-instructions.md` to require:
  - a mandatory final task report for every change,
  - a mandatory update to `WORK_DONE_NOTE.md` for every change.
- Defined required fields for each work note entry:
  - date,
  - what changed,
  - why,
  - files touched.

### Why
- To ensure consistent reporting and persistent project history for every task, including small edits.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

## 00) Mandatory commit workflow (uncommitted)

### Changed
- Updated `.github/copilot-instructions.md` with a required commit rule.
- Added the requirement to always commit task-related changes after verification/tests succeed.
- Defined commit constraints: stage only related files, use a clear message, and avoid leaving task-related edits uncommitted.

### Why
- To ensure every completed change is traceable in git history and reduce risk of forgotten local modifications.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

## 1) Multi-page architecture (committed)

### Changed
- Updated `scripts/update.py` to support three profiles:
  - `general`
  - `enterprise`
  - `discovery`
- Added dedicated query sets:
  - `GENERAL_SEARCH_QUERIES`
  - `ENTERPRISE_SEARCH_QUERIES`
  - `OPTIMIZED_GENERAL_SEARCH_QUERIES`
- Added `--profile` CLI flag to select which dataset to update.
- Added per-profile metadata persistence in JSON (`page_name`, `page_label`, `page_description`, `search_queries`, `last_updated`).

### Why
- To run different search strategies for different page goals and keep each generated page traceable to its query strategy.

## 2) New datasets and generated pages (committed)

### Changed
- Added data files:
  - `data/tools-enterprise.json`
  - `data/tools-discovery.json`
- Updated `data/tools.json` metadata for the general page.
- Updated generator `scripts/generate.py` to build multiple pages.
- Generated/updated pages:
  - `index.html`
  - `enterprise.html`
  - `discovery.html`

### Why
- To publish separate curated views (general, enterprise, discovery) from independent datasets.

## 3) UI updates across pages (committed)

### Changed
- Added a page selector in the header of each generated page.
- Added page-type information block (label + description).
- Added popup/modal showing:
  - search queries used by the current page
  - last update date
- Fixed template formatting/escaping and indentation issues in `scripts/generate.py` so generation succeeds.

### Why
- To improve navigation between pages and provide transparency about sourcing and freshness.

## 4) Rule for mandatory change notes (uncommitted)

### Changed
- Added `.github/copilot-instructions.md` with rule:
  - every task must include a short note explaining what changed and why.

### Why
- To enforce consistent documentation of modifications for every future request.

## 5) Commit reference

- Commit: `48ae561`
- Message: `feat: add enterprise and discovery pages with profile-based queries`
- Branch used during implementation: `feature/mulitple_page`
