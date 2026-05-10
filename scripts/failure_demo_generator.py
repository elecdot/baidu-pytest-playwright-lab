from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect, sync_playwright


def main() -> None:
    output_dir = Path("test-results/failure-demo")
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(locale="zh-CN")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.goto("https://map.baidu.com", wait_until="domcontentloaded")
        try:
            expect(
                page.get_by_text("THIS_TEXT_IS_EXPECTED_TO_BE_ABSENT")
            ).to_be_visible(timeout=2_000)
        except (AssertionError, PlaywrightTimeoutError) as error:
            page.screenshot(
                path=output_dir / "failure-demo-missing-text.png",
                full_page=True,
            )
            (output_dir / "failure-summary.txt").write_text(
                "Controlled failure demo: intentionally waited for missing text on "
                "https://map.baidu.com. This artifact demonstrates Playwright "
                f"failure diagnosis with screenshot and trace.\n\n{error}\n",
                encoding="utf-8",
            )
        finally:
            context.tracing.stop(path=output_dir / "failure-demo-trace.zip")
            context.close()
            browser.close()

    print("failure demo artifacts written to test-results/failure-demo")


if __name__ == "__main__":
    main()
