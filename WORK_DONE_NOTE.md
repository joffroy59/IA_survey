# Work Done Note

Date: 2026-04-17
Repository: IA_survey

## FIX) Apply column mode to top-level categories

### Changed
- Moved column layout target from subcategory groups to top-level categories.
- Added a new `.categories-grid` wrapper in the page template and mapped `data-grid-columns` (`1|2|3`) to this grid.
- Removed the previous `.category-columns` wrapper/layout from category rendering.
- Regenerated all HTML pages and snapshots.

### Why
- User requested that `2` column mode places major categories side by side (for example: `IA Generiques` and `IA Specialisees`).
- Previous implementation was splitting subcategories instead of main categories.

### Files touched
- `scripts/generate.py`
- Generated pages/data/snapshots
- `WORK_DONE_NOTE.md`

## FIX) Remove now mode and apply columns to categories

### Changed
- Removed `now` from column layout toggle cycle. The button now cycles only: `1 -> 2 -> 3 -> 1`.
- Changed grid-column behavior so the toggle applies to category blocks (subcategories) via `.category-columns` instead of tool cards.
- Updated category rendering to wrap subcategories inside a new `.category-columns` container.
- Updated responsive CSS so category columns collapse to one column on small screens.
- Updated layout toggle label/title logic to reflect category columns and current numeric mode.
- Regenerated all HTML pages and snapshots.

### Why
- User requested to remove `now` mode entirely.
- User requested column behavior based on categories, with one category per column.

### Files touched
- `scripts/generate.py`
- Generated pages/data/snapshots
- `WORK_DONE_NOTE.md`

## FEATURE) Convert column layout to toggle button + add button darkening + add page label indicator

### Changed
- **Column Layout Toggle**: Converted from `<select>` dropdown to a toggle button (⊞) that cycles through: 1 → now → 2 → 3 → 1.
- **Button Darkening**: Added CSS `button[aria-pressed="false"]` styling (opacity: 0.5, filter: brightness(0.7)) so toggle buttons appear darkened when their associated elements are hidden.
- **Page Label Indicator**: Added `.current-page-label` element showing current page slug (e.g., "general", "enterprise") that auto-hides when menu is visible and shows when menu is hidden.
- Updated `scripts/generate.py`:
  - Replaced layout selector HTML with layout-columns-toggle button
  - Added `.layout-columns-toggle` and `.current-page-label` CSS
  - Added `button[aria-pressed="false"]` CSS for darkened button state
  - Added `cycleLayoutColumns()` function to cycle through layout options
  - Added `updateLayoutToggle()` to manage layout button state
  - Added `updateAllButtonStates()` master function to sync button states and page label visibility
  - Added `page_slug` template parameter to HTML_TEMPLATE.format()
  - Removed old `.layout-selector-wrap`, `.layout-selector-label`, `.layout-select` CSS

### Why
- User requested: column layout as a toggle button (not a dropdown), matching other UI controls
- Darkening toggle buttons provides visual feedback when associated content is hidden
- Page label keeps users informed of current page even when menu navigation is hidden for more screen space

### Files touched
- `scripts/generate.py`

---

## FEATURE) Add selector for 1/now/2/3 column layout

### Changed
- Added a layout selector in the header action area with options: `1`, `now`, `2`, `3`.
- Updated `scripts/generate.py` CSS to support forced grid column counts via `body[data-grid-columns]`.
- Kept responsive behavior on small screens by capping the 3-column choice to 2 columns on mobile.
- Added JavaScript state persistence with localStorage key `gridColumnsLayout`.
- Regenerated all HTML pages and related snapshots.

### Why
- User requested a selector to switch between `1`, current (`now`), `2`, or `3` columns.
- Persisting the choice keeps the preferred layout across refreshes.

### Files touched
- `scripts/generate.py`
- Generated pages/data/snapshots
- `WORK_DONE_NOTE.md`

### Verification
- Ran `python scripts/generate.py` successfully.
- Verified generated template and output include `layout-columns-select`, `gridColumnsLayout`, and `data-grid-columns` logic.

## FEATURE) Add toggle to hide menu

### Changed
- Added a new `menu-toggle` button in the header to control menu visibility.
- Updated `scripts/generate.py` template to hide/show both:
  - header page switcher (`.page-switcher`)
  - category navigation tabs (`#category-nav`)
- Added persisted state in localStorage with key `menuVisible`.
- Regenerated all HTML pages and related data snapshots.

### Why
- User requested a toggle to hide the menu for a cleaner page layout.
- Persisted state keeps user preference across refreshes.

### Files touched
- `scripts/generate.py`
- Generated pages/data/snapshots
- `WORK_DONE_NOTE.md`

### Verification
- Ran `python scripts/generate.py` successfully.
- Verified generated template and output include `menu-toggle`, `category-nav`, and `menuVisible` logic.

## FEATURE) Add toggle to hide page-meta and audience-brief panels

### Changed
- Added `.panel-toggle` button in header next to theme toggle button
- Added CSS `.hidden` class for `.page-meta` and `.audience-brief` with `display: none`
- Implemented JavaScript functionality to toggle panel visibility
- Persists visibility preference in localStorage with key `panelsVisible`
- Added smooth transitions (0.3s) on panel visibility changes
- Proper ARIA labels for accessibility

### Why
- Users requested ability to hide the "Type de page" and "Public cible" panels for a cleaner view
- Allows customization while maintaining default visible state
- Preference saved across page refreshes

### Files touched
- `scripts/generate.py` - Added CSS, HTML button, and JavaScript logic
- All generated HTML pages with the new toggle feature
- `WORK_DONE_NOTE.md`

### Verification
- Ran `python scripts/generate.py` - all pages generated successfully
- Verified toggle button appears in header (📋 icon)
- Verified panels hide/show on toggle click
- Checked localStorage persistence works correctly
- Verified accessibility attributes (aria-pressed, aria-label) update on toggle

## FIX) Use boolean for static page config and fix class name concatenation

### Changed
- Updated `scripts/generate.py` PAGE_CONFIGS to use boolean `True` instead of string `"true"` for the "static" key
- Fixed `render_page_switcher()` function to properly set class name `"page-link-static"` instead of concatenating to create invalid `"page-linkstatic"`

### Why
- Python booleans should be used for configuration values, not strings
- CSS class names need proper hyphenation: `.page-link-static` not `.page-linkstatic`
- User identified that the static page styling was not applying correctly due to invalid class names

### Files touched
- `scripts/generate.py`
- All generated HTML pages (regenerated with correct styling)
- `WORK_DONE_NOTE.md`

### Verification
- Ran `python scripts/generate.py` - all pages generated successfully
- Verified `ia-resources.html` page has correct class `page-link-static active`
- CSS styling now applies correctly to static pages

## FEATURE) Add IA Resources page with static links

### Changed
- Created `data/tools-ia-resources.json` with static links configuration
- Updated `scripts/generate.py` to include new page configuration for IA Resources
- Generated `ia-resources.html` page from the JSON configuration

### Why
- User requested a new page to display static links (IA Models: https://models.dev/) with easy management through JSON file
- Follows the existing pattern of other pages in the project for consistency

### Files touched
- `data/tools-ia-resources.json` (new file)
- `scripts/generate.py`
- `ia-resources.html` (generated)

### Verification
- Ran `python scripts/generate.py` - all pages generated successfully including the new `ia-resources.html`
- Verified the new page is accessible and displays the link correctly

## FIX) Disable blocking on query-count mismatch in page checker

### Changed
- Updated `scripts/check_pages.py` query validation so `expected 10 queries, found N` is now reported as a warning instead of an error.
- Updated checker header comment to reflect non-blocking behavior for query-count mismatch.

### Why
- User requested that this specific validation issue must not block execution/CI when profiles contain more than 10 queries.

### Files touched
- `scripts/check_pages.py`
- `WORK_DONE_NOTE.md`

### Verification
- `python scripts/check_pages.py`
- Confirmed output shows `Errors: 0` and query-count mismatches listed under warnings.

## DOC) Require feature branches from develop, keep hotfix from main

### Changed
- Updated GitFlow requirements in `.github/copilot-instructions.md` to explicitly require creating every `feature/...` branch from `develop`.
- Kept hotfix flow unchanged: `hotfix/...` branches must still be created from `main`.
- Renumbered the GitFlow checklist items after inserting the new explicit feature branch origin rule.

### Why
- User requested a clear, explicit rule: feature branches from `develop`, while hotfix branches remain from `main`.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

### Verification
- Manual review of `GitFlow Branch Rule (Required)` in `.github/copilot-instructions.md` confirms:
  - feature branch origin is `develop`
  - hotfix branch origin is `main`

## FIX) Rename cowork view label and adjust cowork query wording

### Changed
- Renamed the cowork navigation/page label from `Vue Cowork` to `vue Claude Cowork` in the page generation config.
- Updated generated root HTML pages so the visible navigation now shows `vue Claude Cowork`.
- Updated cowork query metadata label from `Cowork AI` to `Claude Cowork AI`.
- Updated the first cowork query text from `AI cowork collaboration platforms for teams 2026` to `Claude cowork collaboration platforms for teams 2026`.

### Why
- User requested renaming `Vue Cowork` to `vue Claude Cowork` and also asked to change the query wording accordingly.

### Files touched
- `scripts/generate.py`
- `data/search_queries.json`
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
- `aicliapps.html`
- `WORK_DONE_NOTE.md`

### Verification
- `rg -n "Vue Cowork|Claude cowork collaboration platforms for teams 2026|vue Claude Cowork" -g "*.html" -g "!snapshots/**" .`
- Verified no `Vue Cowork` remains in root HTML pages, and new label/query text are present.

## FIX) Add GitFlow hotfix exception flow (main first, then develop)

### Changed
- Updated `.github/copilot-instructions.md` GitFlow requirements to define a dedicated hotfix path:
  - hotfix branch must be created from `main`,
  - first PR must be hotfix branch -> `main`,
  - second PR must be `main` -> `develop` after the hotfix merge.
- Kept feature flow as develop-first and clarified the split between feature and hotfix behavior.
- Added a hotfix note in the `"Finish Feature"` section so hotfix completion uses the hotfix sequence.

### Why
- User requested an exception to the previous rule for hotfixes: branch from `main`, then PR to `main` and to `develop` as GitFlow hotfix.
- This matches standard GitFlow hotfix promotion while preserving develop-first flow for feature work.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

### Verification
- Manual review of `.github/copilot-instructions.md` sections:
  - `GitFlow Branch Rule (Required)`
  - `"Finish Feature" Rule (Required)`

## FIX) Enforce develop-first PR workflow before main

### Changed
- Updated `.github/copilot-instructions.md` GitFlow requirements to enforce:
  - first PR from feature/hotfix branch to `develop`,
  - second PR from `develop` to `main` only after the first merge,
  - no direct feature/hotfix PR to `main`.
- Updated the `"Finish Feature"` rule to follow the same two-step merge sequence.

### Why
- User requested a strict merge-request flow: always merge into `develop` first, then promote `develop` to `main` after the first PR is done.
- This keeps release promotion explicit and aligned with GitFlow.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

### Verification
- Manual review of `.github/copilot-instructions.md` sections:
  - `GitFlow Branch Rule (Required)`
  - `"Finish Feature" Rule (Required)`

## FIX) Accept expanded per-profile query lists in update loader

### Changed
- Updated `scripts/update.py` query validation rule in `load_search_queries()`:
  - replaced strict `exactly 10` requirement with `at least 10`.
- Kept existing protections for empty lists and duplicate queries.

### Why
- The pipeline failed with `ValueError: Profile 'general' must define exactly 10 queries, found 13` after query enrichment.
- Allowing 10+ queries preserves enriched profiles while still enforcing a minimum quality baseline.

### Files touched
- `scripts/update.py`
- `WORK_DONE_NOTE.md`

### Verification
- `python -c "import importlib.util, pathlib; p=pathlib.Path('d:/dev-data/githome/github/joffroy59/IA_survey/scripts/update.py'); s=importlib.util.spec_from_file_location('upd', p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); q=m.load_search_queries(); print('general', len(q['general'])); print('agentdev', len(q['agentdev'])); print('ok')"`
- `python -m py_compile scripts/update.py`

## CI) Add page checker to update pipeline

### Changed
- Updated `.github/workflows/update.yml` to run `python scripts/check_pages.py` right after page generation in the `generate-and-commit` job.

### Why
- User requested adding checker execution in CI to verify generated pages/datasets and reduce risk of unknown or invalid tool entries reaching published pages.

### Files touched
- `.github/workflows/update.yml`
- `WORK_DONE_NOTE.md`

### Verification
- `python scripts/check_pages.py`

## REFACTOR) Global query review + page quality checker + professional dual-audience content

### Changed
- Reworked `data/search_queries.json` so each profile now contains exactly 10 focused, theme-driven queries.
- Updated `scripts/update.py`:
  - enforced exactly 10 unique queries per profile at load time,
  - added a tool quality gate to reject low-confidence names and invalid/non-product URLs before insertion.
- Added `scripts/check_pages.py` to validate:
  - query count/quality,
  - tool URL and naming credibility,
  - rendered HTML tool-card count vs JSON data.
- Enhanced `scripts/generate.py` and regenerated all pages:
  - introduced professional audience briefing blocks for two reader types (developers and managers),
  - synchronized displayed page queries from `data/search_queries.json` as source-of-truth during generation.
- Regenerated HTML pages and snapshots for all profiles.

### Why
- User requested a global review/refactor of queries for better results, with 10 queries per page theme.
- User requested an automated checker to detect page/tool quality issues and avoid unknown/unreliable tool entries.
- User requested more professional content and explicit adaptation for two audiences: technical (dev) and decision-makers (manager).

### Files touched
- `data/search_queries.json`
- `scripts/update.py`
- `scripts/generate.py`
- `scripts/check_pages.py`
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
- `aicliapps.html`
- `data/tools.json`
- `data/tools-enterprise.json`
- `data/tools-discovery.json`
- `data/tools-ragdev.json`
- `data/tools-agentdev.json`
- `data/tools-vscode.json`
- `data/tools-newrag.json`
- `data/tools-cowork.json`
- `data/tools-ocr.json`
- `data/tools-dococr.json`
- `data/tools-aicliapps.json`
- `snapshots/*`
- `WORK_DONE_NOTE.md`

### Verification
- `python scripts/generate.py`
- `python scripts/check_pages.py`
- `python -m py_compile scripts/generate.py scripts/update.py scripts/check_pages.py`

## CI) Run auto update workflow on develop like main

### Changed
- Updated `.github/workflows/update.yml` trigger to run on `push` for both `main` and `develop` branches.

### Why
- User requested automatic build/deploy-style action execution on `develop` the same way as `main`.

### Files touched
- `.github/workflows/update.yml`
- `WORK_DONE_NOTE.md`

## FIX) Clean AI CLI JSON regeneration from query-only evidence + category validation rule

### Changed
- Refactored `scripts/update.py` for profile `aicliapps` to rebuild dataset from query-only evidence instead of cloning general tools.
- Added dedicated CLI category taxonomy and category/subcategory validation before tool insertion.
- Added fallback extraction improvements:
  - structured DuckDuckGo result parsing
  - known CLI tool detection from query evidence
  - stricter filtering to avoid article-title noise
- Regenerated `data/tools-aicliapps.json` from the defined query set using the new logic.
- Updated `.github/agents/query-page-json-builder.agent.md` with a strict rule to always validate category/subcategory consistency with query evidence.

### Why
- User requested a clean CLI JSON regenerated from queries only and stronger category correctness.
- Validation rules and cleaner extraction reduce misclassified and noisy entries.

### Files touched
- `scripts/update.py`
- `data/tools-aicliapps.json`
- `.github/agents/query-page-json-builder.agent.md`
- `WORK_DONE_NOTE.md`

### Verification
- `python scripts/update.py --profile aicliapps`
- Checked resulting `data/tools-aicliapps.json` structure and category assignments.

Date: 2026-04-16
Repository: IA_survey

## FEATURE) New subject page AI CLI Applications

### Changed
- Added new subject profile `aicliapps` in `data/search_queries.json` with 10 DuckDuckGo queries in French.
- Registered `aicliapps` in `scripts/update.py` and `scripts/generate.py` so dataset updates and HTML generation support the new profile.
- Updated workflow matrices/options/path mappings in:
  - `.github/workflows/update.yml`
  - `.github/workflows/update-profile-unit.yml`
  - `.github/workflows/update-consumer-example.yml`
- Ran `python scripts/update.py --profile aicliapps` to create `data/tools-aicliapps.json` and apply profile metadata.
- Ran `python scripts/generate.py` to generate `aicliapps.html` and refresh linked pages/data/snapshots/history.

### Why
- User requested creation of a page for a new subject.
- The subject-driven profile and workflow wiring ensure the page is generated now and maintained by existing automation later.

### Files touched
- `data/search_queries.json`
- `scripts/update.py`
- `scripts/generate.py`
- `.github/workflows/update.yml`
- `.github/workflows/update-profile-unit.yml`
- `.github/workflows/update-consumer-example.yml`
- `data/tools-aicliapps.json`
- `aicliapps.html`
- Regenerated data/pages/snapshots for existing profiles via `scripts/generate.py`
- `WORK_DONE_NOTE.md`

### Verification
- `python -m py_compile scripts/update.py scripts/generate.py`
- `python scripts/update.py --profile aicliapps`
- `python scripts/generate.py`

Date: 2026-04-16
Repository: IA_survey

## ADD) Query/Page/JSON custom agent for subject-driven DuckDuckGo workflow

### Changed
- Created `.github/agents/query-page-json-builder.agent.md`.
- Added a dedicated custom agent that asks the user for a subject, proposes DuckDuckGo queries, and guides JSON/page generation steps for this repository.

### Why
- User requested an agent that helps create a new JSON and page from a subject, with explicit user prompting and DuckDuckGo query generation.
- This makes the workflow repeatable and consistent for future profile additions.

### Files touched
- `.github/agents/query-page-json-builder.agent.md`
- `WORK_DONE_NOTE.md`

Date: 2026-04-16
Repository: IA_survey

## ADD) Mandatory GitFlow branch rule in repository instructions

### Changed
- Updated `.github/copilot-instructions.md` with a new required section: GitFlow Branch Rule.
- Added explicit requirements to always create a dedicated branch per task and avoid direct work on `main` and `develop`.

### Why
- User requested a clear rule to always create a git branch and follow GitFlow workflow.
- This reduces integration risk and keeps branch strategy consistent for all future tasks.

### Files touched
- `.github/copilot-instructions.md`
- `WORK_DONE_NOTE.md`

Date: 2026-04-16
Repository: IA_survey

## ADD) Maintainability-focused custom agent

### Changed
- Created `.github/agents/maintainability-guardian.agent.md`.
- Added a focused custom agent definition for code maintenance work with best-practice guardrails (small scoped changes, readability, API safety, duplication reduction, and verification expectations).

### Why
- User requested an agent specialized in maintaining code with maintainability best practices.
- A reusable custom agent helps apply consistent standards across future maintenance tasks.

### Files touched
- `.github/agents/maintainability-guardian.agent.md`
- `WORK_DONE_NOTE.md`

### Verification
- Verified frontmatter is present and valid-looking (`description`, `tools`, `argument-hint`, invocation settings).

Date: 2026-04-15
Repository: IA_survey

## FEAT) GitLab CI/CD pipeline for Pages build & deploy

### Changed
- Created `.gitlab-ci.yml` with 4 stages (update, generate, build, deploy) adapting all 3 GitHub Actions workflows to GitLab CI.
- Supports: push-to-main deploy, weekly scheduled updates, manual single/all profile updates.

### Why
- Provide a GitLab-compatible alternative for building and deploying generated HTML pages via GitLab Pages.

### Files touched
- `.gitlab-ci.yml`
- `WORK_DONE_NOTE.md`

## DOC) SharePoint deploy plan

### Changed
- Created `SHAREPOINT_DEPLOY_PLAN.md` with 5 integration options for publishing HTML pages to enterprise SharePoint via GitHub Actions.

### Why
- Document the plan and possibilities for deploying generated pages to SharePoint.

### Files touched
- `SHAREPOINT_DEPLOY_PLAN.md`
- `WORK_DONE_NOTE.md`

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

## BUGFIX) All pages showed the same tools

### Date
- 2026-04-16

### Changed
- Reworked `scripts/seed_profiles.py` to stop copying the same sequential tool chunks into every profile.
- Added profile-aware deterministic selection logic so each profile gets a distinct subset of tools.
- Regenerated profile datasets:
  - `data/tools-enterprise.json`
  - `data/tools-discovery.json`
  - `data/tools-ragdev.json`
  - `data/tools-agentdev.json`
  - `data/tools-vscode.json`
  - `data/tools-newrag.json`
  - `data/tools-cowork.json`
  - `data/tools-ocr.json`
  - `data/tools-dococr.json`
- Regenerated profile pages:
  - `enterprise.html`
  - `discovery.html`
  - `ragdev.html`
  - `agentdev.html`
  - `vscode.html`
  - `newrag.html`
  - `cowork.html`
  - `ocr.html`
  - `dococr.html`

### Why
- The previous seeding approach distributed tools from a single general list in the same pattern, causing multiple pages to display effectively the same tools.
- The new selection strategy ensures profile pages are differentiated while keeping deterministic generation.

### Files touched
- `scripts/seed_profiles.py`
- `data/tools-enterprise.json`
- `data/tools-discovery.json`
- `data/tools-ragdev.json`
- `data/tools-agentdev.json`
- `data/tools-vscode.json`
- `data/tools-newrag.json`
- `data/tools-cowork.json`
- `data/tools-ocr.json`
- `data/tools-dococr.json`
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
- `python -m py_compile scripts/seed_profiles.py`
- `python scripts/seed_profiles.py`
- `python scripts/generate.py`
- Verified key profile pairs are no longer identical:
  - `tools-enterprise.json` vs `tools-discovery.json` => different
  - `tools-enterprise.json` vs `tools-ragdev.json` => different
  - `tools-cowork.json` vs `tools-ocr.json` => different
  - `tools-cowork.json` vs `tools-vscode.json` => different
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

## QUERY UPDATE) Add mandatory tool discovery queries (English-only)

### Date
- 2026-04-16

### Changed
- Updated [data/search_queries.json](data/search_queries.json) to improve discovery for mandatory tools:
  - Gemini CLI
  - OpenCode
  - OpenClaw
  - Hermes
  - Gemini Code Assist
  - Docling
  - Codex
  - Claude
  - Claude Code
  - GitHub Copilot
  - OpenAI
  - broader AI CLI tool discovery
- Added explicit mandatory-tool queries to profiles where they are most relevant:
  - `agentdev`
  - `vscode`
  - `aicliapps`
  - `ragdev` / `newrag` / `ocr` / `dococr` for Docling-focused coverage
- Replaced remaining non-English query lines with English equivalents for better DuckDuckGo retrieval quality.

### Why
- Ensure update jobs discover required mandatory tools consistently.
- Align query language with DuckDuckGo performance expectations (English-first).
- Improve profile-specific relevance by targeting each mandatory tool to matching page intent.

### Files touched
- [data/search_queries.json](data/search_queries.json)
- [WORK_DONE_NOTE.md](WORK_DONE_NOTE.md)

### Verification
- Parsed [data/search_queries.json](data/search_queries.json) with Python JSON loader successfully (`OK`).
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
