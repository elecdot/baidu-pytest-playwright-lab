# Baidu Map Pytest Playwright Test Lab

Python Playwright automation lab for the Baidu Map Web application. The project
uses `uv`, `pytest`, `pytest-playwright`, and Page Object Model conventions to
build reproducible end-to-end tests and collect classroom-friendly evidence such
as screenshots, traces, videos, and HTML reports.

## Project Overview

<<<<<<< HEAD
### Stack
=======
The target system is the Baidu Map Web client at `https://map.baidu.com`. The
test suite is planned around high-value user flows:
>>>>>>> a5f35de (build: initial commit)

- Home page smoke checks.
- Place search and search result validation.
- Route planning entry points and basic route results.
- Map interactions such as zooming and dragging.
- Geolocation permission and mocked coordinates.
- Desktop and mobile viewport coverage.
- Robustness checks for empty, invalid, and special-character inputs.

The project intentionally avoids high-frequency scraping, bypassing
anti-automation controls, login flows, security scanning, and data accuracy
claims. Tests should stay low volume and focus on observable UI behavior.

## Stack

- Python `3.12`
- `uv` for environment and dependency management
- `pytest` as the test runner
- `pytest-playwright` for browser fixtures and Playwright CLI options
- Playwright for Python for browser automation
- `pytest-html` for self-contained HTML reports
- `ruff` and `pre-commit` for basic quality checks

## Directory Structure

```text
.
├── data/              # Test data modules and data maintenance notes.
├── docs/              # Design book and project documentation.
├── pages/             # Page Object Model wrappers for Baidu Map pages.
├── reports/           # Generated pytest-html reports.
├── scripts/           # Local helper scripts, including agent-safe uv wrapper.
├── test-results/      # Playwright screenshots, traces, videos, and artifacts.
├── tests/             # Pytest test cases grouped by feature.
├── justfile           # Common human and agent commands.
├── pyproject.toml     # Python project metadata, dependencies, and tool config.
└── uv.lock            # Locked dependency graph.
```

See each directory-level `README.md` before adding files in that directory.

## Quick Start

Install dependencies and Playwright browsers:

```bash
uv sync
uv run playwright install
```

Run the full test suite:

```bash
just test
```

Run checks used by Codex or other sandboxed agents:

```bash
just agent-ruff
just agent-format
just agent-test
```

The agent commands use `./scripts/agent-env.sh` so `uv` writes its cache inside
the workspace instead of a read-only sandbox cache path.

## Common Commands

```bash
just ruff
just format
just test
just test-headed
just agent-ruff
just agent-format
just agent-test
uv run pytest tests/test_home.py
uv run pytest --browser chromium --headed
uv run playwright codegen https://map.baidu.com
```

Generated reports and runtime artifacts are written to `reports/` and
`test-results/`.

## Documentation

- [docs/design_book.md](docs/design_book.md) - Overall experimental design,
  scope, strategy, test cases, data, execution plan, risks, and report outline.
- [docs/README.md](docs/README.md) - Documentation index and maintenance rules.
- [tests/README.md](tests/README.md) - Test organization and naming rules.
- [pages/README.md](pages/README.md) - Page Object Model conventions.
- [data/README.md](data/README.md) - Test data ownership and update rules.
- [reports/README.md](reports/README.md) - HTML report output guidance.
- [test-results/README.md](test-results/README.md) - Playwright artifact notes.

## Open Loops

- Implement the first Page Object in `pages/baidu_map_page.py`.
- Add structured test data in `data/test_data.py`.
- Add smoke tests before expanding search, route, geolocation, and mobile flows.
- Confirm stable Baidu Map locators through Playwright codegen.
- Keep `docs/design_book.md` synchronized as the executable suite evolves.
