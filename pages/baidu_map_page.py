"""Page Object helpers for the Baidu Map Web application."""

from pathlib import Path

from playwright.sync_api import Page, expect


class BaiduMapPage:
    """Small first-pass Page Object for stable smoke-test interactions."""

    url = "https://map.baidu.com"

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        self.page.goto(self.url, wait_until="domcontentloaded")

    def expect_page_loaded(self) -> None:
        expect(self.page.locator("body")).to_be_visible()

    def screenshot(self, name: str) -> None:
        artifact_dir = Path("test-results")
        artifact_dir.mkdir(exist_ok=True)
        self.page.screenshot(path=artifact_dir / f"{name}.png", full_page=True)
