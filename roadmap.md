# Experiment Roadmap

This roadmap turns the design in `docs/design_book.md` into staged, executable
work. Each stage should end with passing checks, generated evidence, and updated
documentation when behavior changes.

## Stage 0: Project Foundation

Status: complete.

- [x] Create repository documentation and directory-level README files.
- [x] Configure `uv`, `pytest`, `pytest-playwright`, `pytest-html`, `ruff`, and
  `pre-commit`.
- [x] Add `just` commands for human and sandbox-safe agent workflows.
- [x] Configure generated evidence paths:
  - `reports/report.html`
  - `test-results/homepage.png`
  - `test-results/playwright/` for Playwright-managed artifacts.

Exit criteria:

- [x] `just agent-ruff` passes.
- [x] `pytest --markers` shows project markers.

## Stage 1: Minimal Smoke Loop

Status: complete.

- [x] Add structured test data in `data/test_data.py`.
- [x] Add the first Page Object in `pages/baidu_map_page.py`.
- [x] Add `tests/test_home.py` with `@pytest.mark.smoke`.
- [x] Open `https://map.baidu.com`, assert the page body is visible, and capture
  `test-results/homepage.png`.

Exit criteria:

- [x] `just agent-ruff` passes.
- [x] `just agent-test` passes with `1 passed`.
- [x] `reports/report.html` is generated.
- [x] `test-results/homepage.png` is generated.

## Stage 2: Search Flow Under Anti-Automation Constraint

Status: complete.

- [x] Use Playwright codegen or manual exploration to confirm stable search
  locators.
- [x] Extend `BaiduMapPage` with search-oriented helpers:
  - `fill_search_input(keyword: str)`
  - `expect_search_input_value(keyword: str)`
  - `classify_search_suggestion_state(keyword: str)`
  - `search(keyword: str)`
  - `expect_search_or_security_challenge_observed(keyword: str)`
  - `goto_url(url: str)`
- [x] Add `tests/test_search.py` with three anti-automation-aware tests:
  - search input accepts `北京大学`
  - search suggestion state is classified instead of forced
  - search result state is classified for submission and known result URL
- [x] Treat either a search result or Baidu security challenge as an observed
  search outcome.
- [x] Treat headless map URL navigation after Enter as an observed submission
  outcome when result text and security challenge are absent.
- [x] Keep assertions resilient: verify visible page text or stable result
  indicators, not exact map tiles or live traffic values.

Exit criteria:

- [x] `just agent-ruff` passes.
- [x] `just agent-test` passes with home and search tests.
- [x] Search screenshots or failure artifacts are available under
  `test-results/`.
- [x] `docs/locator_discovery_notes.md` records the security challenge boundary.

## Stage 3: Route Panel Smoke

Status: complete.

- [x] Use codegen to confirm route entry, start input, and end input locators.
- [x] Add route panel helpers to `BaiduMapPage`:
  - `open_route_panel()`
  - `expect_route_panel_open()`
  - `route_entry`
  - `route_start_input`
  - `route_end_input`
- [x] Add `tests/test_route.py` with `test_route_panel_can_be_opened`.
- [x] Verify route entry is clickable and the route panel exposes start/end
  inputs or transport-mode labels.
- [x] Defer start/end entry and route result assertions to a later route-planning
  stage because Stage 3A only covers panel smoke behavior.

Exit criteria:

- [x] Route panel smoke passes in Chromium.
- [x] `test-results/route-panel-open.png` is generated.
- [x] `docs/locator_discovery_notes.md` records the route entry boundary.
- [x] No assertions depend on exact route duration, distance, price, or traffic
  state.

## Stage 4: Geolocation And Mobile Smoke

Status: planned.

- [ ] Add geolocation tests using explicit browser context permissions and
  mocked coordinates from `GEO_LOCATIONS`.
- [ ] Add one mobile viewport smoke test with touch/mobile context settings.
- [ ] Keep mobile and geolocation assertions limited to page stability and
  visible handling.

Exit criteria:

- [ ] Geolocation smoke test passes or documents browser/environment limitation.
- [ ] Mobile smoke test passes.
- [ ] Report and screenshot artifacts are generated.

## Stage 5: Evidence, Analysis, And Final Report

Status: planned.

- [ ] Run the stable suite and archive key evidence paths in the experiment
  report.
- [ ] Fill the execution summary, defect record, and flaky-test record templates
  from `docs/design_book.md`.
- [ ] Analyze Playwright strengths and limits for complex map applications.
- [ ] Keep generated artifacts out of git unless explicitly needed for the final
  submission.

Exit criteria:

- [ ] Final report can reference passing tests, failures, screenshots, trace
  files, and HTML report output.
- [ ] README and design book match the implemented scope.
- [ ] Remaining risks and skipped scenarios are clearly documented.

## Operating Rules

- Prefer small, stable increments over broad coverage.
- Use codegen for locator discovery, but move only reviewed locator strategies
  into Page Objects.
- Do not bypass login, captcha, permission, or anti-automation controls.
- Do not perform high-frequency scraping or load testing against the public site.
- Treat external website instability as an experiment finding when it is backed
  by screenshots, trace files, or report output.
