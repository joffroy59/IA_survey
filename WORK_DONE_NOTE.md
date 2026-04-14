# Work Done Note

Date: 2026-04-15
Repository: IA_survey

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
