import pytest
from playwright.sync_api import Page

from data.test_data import ROUTE_CASES
from pages.baidu_map_page import BaiduMapPage


@pytest.mark.route
def test_route_panel_can_be_opened(page: Page) -> None:
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.open_route_panel()

    baidu_map.expect_route_panel_open()
    baidu_map.screenshot("route-panel-open")


@pytest.mark.route
def test_drive_route_planning_baseline(page: Page) -> None:
    baidu_map = BaiduMapPage(page)
    route_case = ROUTE_CASES[0]

    baidu_map.goto()
    baidu_map.plan_drive_route(route_case["start"], route_case["end"])

    baidu_map.expect_route_results_visible()
    baidu_map.screenshot(f"route-result-{route_case['name']}")

    baidu_map.open_first_route_detail()
    baidu_map.expect_route_detail_visible()
    baidu_map.screenshot(f"route-detail-{route_case['name']}")
