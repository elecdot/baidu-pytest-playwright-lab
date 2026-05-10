"""Page Object helpers for the Baidu Map Web application."""

from pathlib import Path

from playwright.sync_api import (
    Locator,
    Page,
    expect,
)
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)


class BaiduMapPage:
    """Small first-pass Page Object for stable smoke-test interactions."""

    url = "https://map.baidu.com"

    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self) -> None:
        self.page.goto(self.url, wait_until="domcontentloaded")

    def goto_url(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def expect_page_loaded(self) -> None:
        expect(self.page.locator("body")).to_be_visible()

    def search(self, keyword: str) -> str:
        previous_url = self.page.url
        search_input = self.page.get_by_role("textbox", name="搜地点、查公交、找路线")
        expect(search_input).to_be_visible(timeout=15_000)
        search_input.click()
        search_input.fill(keyword)
        expect(search_input).to_have_value(keyword)
        search_input.press("Enter")
        return previous_url

    def expect_text_visible(self, text: str, timeout: int = 15_000) -> None:
        expect(self.page.get_by_text(text).first).to_be_visible(timeout=timeout)

    def expect_search_or_security_challenge_observed(
        self,
        keyword: str,
        previous_url: str | None = None,
        timeout: int = 20_000,
    ) -> str:
        challenge = self.security_challenge_indicator
        result = self.page.get_by_text(keyword).first
        try:
            expect(challenge.or_(result).first).to_be_visible(timeout=5_000)
        except (AssertionError, PlaywrightTimeoutError):
            if previous_url is None:
                raise
            expect(self.page).not_to_have_url(previous_url, timeout=timeout)
            return "map_navigation"

        if challenge.first.is_visible():
            return "security_challenge"
        return "result"

    @property
    def security_challenge_indicator(self) -> Locator:
        return self.page.get_by_text("百度安全验证").or_(
            self.page.get_by_text("请完成下方验证后继续操作")
        )

    def screenshot(self, name: str) -> None:
        artifact_dir = Path("test-results")
        artifact_dir.mkdir(exist_ok=True)
        self.page.screenshot(path=artifact_dir / f"{name}.png", full_page=True)
