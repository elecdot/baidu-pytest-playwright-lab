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

## Stage 2: Search Flow

Status: next.

- [ ] Use Playwright codegen or manual exploration to confirm stable search
  locators.
- [ ] Extend `BaiduMapPage` with search-oriented helpers:
  - `search(keyword: str)`
  - `expect_text_visible(text: str, timeout: int = 15_000)`
  - optional screenshot naming for search evidence.
- [ ] Add `tests/test_search.py` with a small first set:
  - one valid P0 keyword such as `北京大学`
  - one invalid input robustness check.
- [ ] Keep assertions resilient: verify visible page text or stable result
  indicators, not exact map tiles or live traffic values.

Exit criteria:

- [ ] `just agent-ruff` passes.
- [ ] `just agent-test` passes with home and search tests.
- [ ] Search screenshots or failure artifacts are available under
  `test-results/`.
- [ ] README Open Loops and `docs/design_book.md` are updated if scope changes.

## Stage 3: Route Planning Baseline

Status: planned.

- [ ] Use codegen to confirm route entry, start input, end input, and submit
  locators.
- [ ] Add route helpers to `BaiduMapPage` only after locator behavior is
  observed.
- [ ] Add a small route baseline test for one P0 route, such as 北京南站 to
  天安门广场.
- [ ] Avoid asserting exact duration, distance, price, or traffic state.

Exit criteria:

- [ ] Route baseline passes in Chromium.
- [ ] Failure artifacts are useful enough to diagnose locator instability.
- [ ] Flaky behavior is recorded instead of hidden.

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
