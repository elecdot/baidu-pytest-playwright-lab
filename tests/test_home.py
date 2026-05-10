import pytest
from playwright.sync_api import Page

from pages.baidu_map_page import BaiduMapPage


@pytest.mark.smoke
def test_homepage_can_be_opened(page: Page) -> None:
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.expect_page_loaded()
    baidu_map.screenshot("homepage")
