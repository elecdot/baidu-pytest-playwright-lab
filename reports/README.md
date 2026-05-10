# Reports

This directory is reserved for generated pytest HTML reports.

## Expected Output

The default report path is planned as:

```text
reports/report.html
```

Reports summarize executed tests, failures, durations, and captured metadata.
Use them as final experiment evidence together with screenshots and traces from
`test-results/`.

## Conventions

- Do not hand-edit generated report files.
- Keep this README tracked so the directory exists in a fresh checkout.
- Treat generated reports as reproducible artifacts, not source files.
- Regenerate reports when test scope, browser configuration, or evidence changes.

## Viewing

On Linux or WSL:

```bash
xdg-open reports/report.html
```
