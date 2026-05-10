import pytest
from playwright.sync_api import Page

from pages.baidu_map_page import BaiduMapPage


@pytest.mark.route
def test_route_panel_can_be_opened(page: Page) -> None:
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.open_route_panel()

    baidu_map.expect_route_panel_open()
    baidu_map.screenshot("route-panel-open")
