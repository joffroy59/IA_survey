# Work Done Note

Date: 2026-04-15
Repository: IA_survey

## ADD) Docling search queries for OCR, DocOCR, New RAG, RAG Dev profiles

### Changed
- Added docling-related search queries to 4 profiles in `data/search_queries.json`:
  - **ocr** (+2): `docling document parsing OCR python 2026`, `docling IBM open source document processing`
  - **dococr** (+2): `docling document processing pipeline OCR parsing 2026`, `docling vs unstructured document ai comparison`
  - **newrag** (+1): `docling document parsing for RAG pipeline 2026`
  - **ragdev** (+1): `docling document parsing RAG ingestion pipeline 2026`
- Synced queries to the 4 profile JSON data files.

### Why
- Docling (IBM open-source document processing) is highly relevant for OCR, document processing, and RAG ingestion pipelines but was missing from search queries.

### Files touched
- `data/search_queries.json`
- `data/tools-ocr.json`
- `data/tools-dococr.json`
- `data/tools-newrag.json`
- `data/tools-ragdev.json`
- `WORK_DONE_NOTE.md`

## FIX) Seed missing profiles — vscode, newrag, cowork, ocr, dococr

### Changed
- Fixed `scripts/seed_profiles.py`: added the 5 missing profiles (vscode, newrag, cowork, ocr, dococr) to the seeding list and removed duplicated script code.
- Ran seeding to populate all 5 JSON data files with tools from the general profile (24 tools each: 3 per subcategory × 8 subcategories).
- Regenerated all 5 HTML pages via `generate.py` so tool cards are now rendered.
- Verified locally: all categories/subcategories match between JSON and HTML, all pages pass.

### Why
- The 5 views (VS Code, New RAG, Cowork, OCR, OCR Système Complet) displayed 0 tools because their JSON files had empty `tools: []` arrays — `seed_profiles.py` only seeded 4 profiles out of 9.

### Files touched
- `scripts/seed_profiles.py`
- `data/tools-vscode.json`
- `data/tools-newrag.json`
- `data/tools-cowork.json`
- `data/tools-ocr.json`
- `data/tools-dococr.json`
- `vscode.html`
- `newrag.html`
- `cowork.html`
- `ocr.html`
- `dococr.html`
- `WORK_DONE_NOTE.md`

---

Date: 2026-04-15
Repository: IA_survey

## RELEASE) Merge and release prep refresh

### Changed
- Consolidated pending updates across generated pages and snapshots for all views.
- Included compare view and VS Code dataset updates in the release content set.

### Why
- User requested merge and release; all pending tracked changes must be committed before merge.
- Keeping generated HTML/data/snapshots aligned ensures release artifacts are consistent.

### Files touched
- `index.html`
- `enterprise.html`
- `discovery.html`
- `ragdev.html`
- `agentdev.html`
- `vscode.html`
- `newrag.html`
- `cowork.html`
- `ocr.html`
- `dococr.html`
- `compare-view.html`
- `data/tools-vscode.json`
- `snapshots/*`
- `WORK_DONE_NOTE.md`

### Verification
- Checked git status to confirm all pending tracked changes are included in release commit scope.

## FIX) Light theme readability and contrast

### Changed
- Reworked title gradient contrast so the heading stays readable in light mode (`var(--text)` start color instead of pure white).
- Replaced hardcoded dark header panel backgrounds with theme-aware surfaces:
  - `.page-switcher` now uses `var(--surface)`
  - `.page-meta` now uses `var(--surface)`
- Updated generator template with the same contrast rules so future page generations keep the fix.

### Why
- In light mode, some components stayed visually dark and the first letters of "Boîte à outils IA Génératives" became hard to read due to white-on-light gradient.
- The fix ensures consistent readability and visual coherence between dark and light themes.

### Files touched
- `scripts/generate.py`
- `index.html`
- `enterprise.html`
- `discovery.html`
- `ragdev.html`
- `agentdev.html`
- `vscode.html`
- `newrag.html`
- `cowork.html`
- `ocr.html`
- `dococr.html`
- `WORK_DONE_NOTE.md`

### Verification
- Checked updated CSS in generated pages (including `vscode.html`) to confirm:
  - readable heading gradient in light mode
  - no dark hardcoded panel backgrounds for page switcher/meta blocks

## FEATURE) Add dark/light mode toggle to all pages

### Changed
- Added CSS variables for light mode theming to all main HTML files
- Added theme toggle button (☀️/🌙) positioned in top-right of header
- Implemented localStorage persistence for theme preference
- Updated styles for light mode with complementary color palette:
  - Light backgrounds (#f8f7fc, #ffffff)
  - Dark text (#1a1620)
  - Adjusted borders and muted colors for light mode
- Added JavaScript functionality for theme switching and icon updates
- Button styling with hover effects and smooth transitions

### Why
- Users requested ability to toggle between dark and light mode for better accessibility and user preference support.
- Persistent storage ensures theme preference is remembered across sessions.
- Consistent implementation across all pages for seamless user experience.

### Files touched
- `index.html`
- `enterprise.html`
- `discovery.html`
- `ragdev.html`
- `agentdev.html`
- `vscode.html`
- `newrag.html`
- `cowork.html`
- `ocr.html`
- `dococr.html`
- `compare-view.html`
- `WORK_DONE_NOTE.md`

### Verification
- All 11 HTML files updated with theme variables and toggle functionality
- Light mode colors tested for readability and contrast
- localStorage integration verified for persistence
- Theme toggle button positioned correctly in all page headers

## FEATURE) Add OCR page and complete OCR document system page

### Changed
- Added two new profiles and pages:
  - `ocr` -> `ocr.html` + `data/tools-ocr.json`
  - `dococr` -> `dococr.html` + `data/tools-dococr.json`
- Added OCR-focused queries and full document OCR-system queries in `data/search_queries.json`.
- Updated `scripts/update.py` profile config to support both new profiles.
- Updated `scripts/generate.py` page config to generate `ocr.html` and `dococr.html`.
- Updated workflows (`update.yml`, `update-profile-unit.yml`, `update-consumer-example.yml`) to include `ocr` and `dococr` in matrix/options/path/commit stages.
- Regenerated pages and datasets, including snapshot history entries for both new pages.

### Why
- Requirement requested a dedicated OCR tools page and a dedicated page for complete document OCR systems.
- Integrating profiles into update/generate/workflow ensures full automation parity with existing pages.

### Files touched
- `scripts/update.py`
- `scripts/generate.py`
- `data/search_queries.json`
- `data/tools-ocr.json`
- `data/tools-dococr.json`
- `.github/workflows/update.yml`
- `.github/workflows/update-profile-unit.yml`
- `.github/workflows/update-consumer-example.yml`
- Generated outputs: `ocr.html`, `dococr.html`, updated existing pages/datasets, and `snapshots/*`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/update.py scripts/generate.py`
- `python scripts/update.py --profile ocr`
- `python scripts/update.py --profile dococr`
- `python scripts/generate.py`
- Confirmed `ocr.html` and `dococr.html` generated and include standard page features.

## RELEASE PREP) Refresh pages/datasets before v1.3.0

### Changed
- Regenerated all pages and datasets prior to release merge.
- Updated all `data/tools*.json` files and page outputs:
  - `index.html`, `enterprise.html`, `discovery.html`, `ragdev.html`, `agentdev.html`, `vscode.html`, `newrag.html`, `cowork.html`
- Added new snapshot versions under `snapshots/*` for history/compare continuity.

### Why
- Ensure release is published with latest generated state and synchronized history snapshots.

### Files touched
- `data/tools*.json`
- `*.html`
- `snapshots/*`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/update.py scripts/generate.py`
- `python scripts/generate.py`

## FEATURE) VS Code, New RAG, Cowork pages + history compare + ZIP export

### Changed
- Added 3 new profiles/pages:
  - VS Code (`vscode.html`, `data/tools-vscode.json`)
  - New RAG (`newrag.html`, `data/tools-newrag.json`)
  - Cowork (`cowork.html`, `data/tools-cowork.json`)
- Added profile queries in `data/search_queries.json` for `vscode`, `newrag`, and `cowork`.
- Updated `scripts/update.py` profile config so these pages are updatable by workflow.
- Updated workflows (`update.yml`, `update-profile-unit.yml`, `update-consumer-example.yml`) to include new profiles in matrix, manual choices, dataset paths, and auto-commit file lists.
- Upgraded generated pages with:
  - history entries linked to immutable snapshots
  - compare action opening `compare-view.html`
  - ZIP export buttons (`ZIP Page`, `ZIP All`)
  - footer copyright text: "Copyright made by joffroy"
- Added `compare-view.html` and snapshot persistence under `snapshots/<page>/...`.
- Added snapshot pruning logic to keep storage aligned with retained history.

### Why
- Requirement requested dedicated pages for VS Code, New RAG, and Cowork themes.
- Requirement requested clickable history with old-page viewing and comparison.
- Requirement requested downloadable ZIP export (single page or all pages).
- Requirement requested explicit copyright attribution.

### Files touched
- `scripts/generate.py`
- `scripts/update.py`
- `data/search_queries.json`
- `data/tools-vscode.json`
- `data/tools-newrag.json`
- `data/tools-cowork.json`
- `.github/workflows/update.yml`
- `.github/workflows/update-profile-unit.yml`
- `.github/workflows/update-consumer-example.yml`
- Generated pages: `vscode.html`, `newrag.html`, `cowork.html`, `compare-view.html` + existing pages regenerated
- Snapshot files: `snapshots/*`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/generate.py scripts/update.py`
- `python scripts/generate.py`
- `python scripts/update.py --profile vscode`
- `python scripts/update.py --profile newrag`
- `python scripts/update.py --profile cowork`
- Confirmed new pages render ZIP buttons, history compare links, and copyright footer.

## UI) Show total tools and new tools on each page

### Changed
- Updated `scripts/generate.py` to compute:
  - total tools count (`count_tools`)
  - new tools count (`count_new_tools`, based on `new: true`)
- Added a header line in generated pages:
  - `Outils : X · Nouveaux : Y`
- Regenerated all pages:
  - `index.html`
  - `enterprise.html`
  - `discovery.html`
  - `ragdev.html`
  - `agentdev.html`

### Why
- Requirement: display both the total number of tools and the number of new tools on every page for quick visibility.

### Files touched
- `scripts/generate.py`
- `index.html`
- `enterprise.html`
- `discovery.html`
- `ragdev.html`
- `agentdev.html`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/generate.py`
- `python scripts/generate.py`
- Checked all 5 pages contain `Outils : <span>...</span> · Nouveaux : <span>...</span>`

## CI) Remove Node 20 deprecation warning in GitHub Actions

### Changed
- Added workflow-level environment variable `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` in:
  - `.github/workflows/update.yml`
  - `.github/workflows/update-profile-unit.yml`
  - `.github/workflows/update-consumer-example.yml`

### Why
- GitHub Actions warned that Node.js 20-backed JavaScript actions are deprecated.
- Opting in to Node 24 now removes warning noise and avoids future runtime breakage when Node 20 is removed.

### Files touched
- `.github/workflows/update.yml`
- `.github/workflows/update-profile-unit.yml`
- `.github/workflows/update-consumer-example.yml`
- `WORK_DONE_NOTE.md`

### Verification
- Reviewed workflow diffs to confirm `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true` is present at workflow top level in all three files.

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
