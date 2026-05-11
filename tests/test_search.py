import pytest
from playwright.sync_api import Page

from data.test_data import KNOWN_SEARCH_RESULT_PAGES
from pages.baidu_map_page import BaiduMapPage


@pytest.mark.search
def test_search_input_accepts_keyword(page: Page) -> None:
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.fill_search_input("北京大学")

    baidu_map.expect_search_input_value("北京大学")
    baidu_map.screenshot("search-input-keyword")


@pytest.mark.search
def test_search_suggestion_classification_under_anti_automation(page: Page) -> None:
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    baidu_map.fill_search_input("北京大学")

    outcome = baidu_map.classify_search_suggestion_state("北京大学")
    assert outcome in {
        "suggestion",
        "security_challenge",
        "input_retained_without_suggestion",
        "input_cleared",
        "partial_input_retained",
    }
    baidu_map.screenshot(f"search-suggestion-{outcome}")


@pytest.mark.search
def test_search_result_classification_under_anti_automation(page: Page) -> None:
    baidu_map = BaiduMapPage(page)

    baidu_map.goto()
    previous_url = baidu_map.search("北京大学")

    outcome = baidu_map.expect_search_or_security_challenge_observed(
        "北京大学",
        previous_url=previous_url,
    )
    assert outcome in {"result", "security_challenge", "map_navigation"}
    baidu_map.screenshot(f"search-submission-{outcome}")

    baidu_map.goto_url(KNOWN_SEARCH_RESULT_PAGES["北京大学"])
    baidu_map.expect_page_loaded()
    outcome = baidu_map.expect_search_or_security_challenge_observed("北京大学")
    assert outcome in {"result", "security_challenge", "map_navigation"}
    baidu_map.screenshot(f"search-known-result-page-{outcome}")
