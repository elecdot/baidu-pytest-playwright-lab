# Pages

This directory contains Page Object Model classes for Baidu Map UI flows.
Page Objects keep locator choices, waiting behavior, and repeated interactions
out of test files so tests can read like user scenarios.

## Planned Files

- `baidu_map_page.py` for shared home page, search, route, map, and screenshot
  helpers.

## Conventions

- Accept a Playwright `Page` in each Page Object constructor.
- Keep public methods behavior-oriented, for example `goto()`, `search()`, and
  `expect_page_loaded()`.
- Prefer Playwright locators based on role, text, placeholder, labels, or
  visible structure before using brittle CSS selectors.
- Document non-obvious locator fallbacks with short comments because Baidu Map
  has dynamic DOM, popups, and asynchronous rendering.
- Do not put test assertions for business scenarios here unless they are shared
  page-level expectations.

## Locator Workflow

Use Playwright codegen for exploration:

```bash
uv run playwright codegen https://map.baidu.com
```

Move only the stable, reviewed locator strategy into Page Object methods.
