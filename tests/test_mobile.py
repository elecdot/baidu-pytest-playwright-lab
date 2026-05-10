import pytest
from playwright.sync_api import Browser

from pages.baidu_map_page import BaiduMapPage


@pytest.mark.mobile
def test_mobile_viewport_homepage_can_be_opened(browser: Browser) -> None:
    context = browser.new_context(
        viewport={"width": 393, "height": 852},
        is_mobile=True,
        has_touch=True,
        locale="zh-CN",
    )

    try:
        page = context.new_page()
        baidu_map = BaiduMapPage(page)

        baidu_map.goto()
        baidu_map.expect_page_loaded()
        baidu_map.screenshot("mobile-homepage")
    finally:
        context.close()
