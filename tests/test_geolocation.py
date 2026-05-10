import pytest
from playwright.sync_api import Browser

from data.test_data import GEO_LOCATIONS
from pages.baidu_map_page import BaiduMapPage


@pytest.mark.geo
def test_geolocation_beijing_context_can_open_map(browser: Browser) -> None:
    context = browser.new_context(
        geolocation=GEO_LOCATIONS["beijing"],
        permissions=["geolocation"],
        locale="zh-CN",
        timezone_id="Asia/Shanghai",
    )

    try:
        page = context.new_page()
        baidu_map = BaiduMapPage(page)

        baidu_map.goto()
        baidu_map.expect_page_loaded()
        baidu_map.screenshot("geolocation-beijing")
    finally:
        context.close()
