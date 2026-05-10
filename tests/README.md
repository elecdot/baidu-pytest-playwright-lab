# Tests

Pytest test cases live in this directory. Tests should describe user-visible
Baidu Map behavior and delegate page mechanics to Page Object classes in
`pages/`.

## Organization

Planned files:

- `test_home.py` for smoke checks and page-load evidence.
- `test_search.py` for valid, invalid, and broad keyword search flows.
- `test_route.py` for basic route planning flows.
- `test_geolocation.py` for permission and mocked-coordinate coverage.
- `test_mobile.py` for mobile viewport checks.

## Conventions

- Name test files `test_<feature>.py`.
- Name test functions after the behavior under test, not implementation steps.
- Use data from `data/` for repeated cases and parametrized scenarios.
- Keep assertions resilient: verify stable visible outcomes instead of exact
  traffic times, route durations, or dynamic map tile details.
- Add screenshots only for meaningful evidence or failure diagnosis.

## Running

```bash
uv run pytest
uv run pytest tests/test_home.py
uv run pytest --browser chromium --headed
```

Sandboxed agents should prefer:

```bash
just agent-test
```
