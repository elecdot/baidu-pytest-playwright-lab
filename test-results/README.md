# Test Results

This directory is reserved for Playwright runtime artifacts produced by pytest
runs.

## Expected Artifacts

- Screenshots for important evidence and failures.
- Trace archives retained on failure.
- Videos retained on failure when video capture is enabled.
- Temporary Playwright files created during local debugging.

## Conventions

- Do not hand-edit generated artifacts.
- Keep this README tracked so the directory exists in a fresh checkout.
- Use descriptive screenshot names such as `homepage.png` or
  `search-beijing-university.png`.
- Avoid committing large binary artifacts unless they are explicitly needed for
  a report or review.

## Trace Viewer

Open a retained trace with:

```bash
uv run playwright show-trace test-results/path/to/trace.zip
```
