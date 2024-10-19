import re

import pytest
from selenium.webdriver.common.by import By

from src.main.helper.element_helper import ElementHelper
from src.main.pages.home_page import HomePage
from src.main.pages.top_panel_page import TopPanelPage


@pytest.fixture
def element_helper():
    return ElementHelper()


def test_desktops(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    list_of_desktops = desktops_page.get_list_of_desktops()

    expected_count = 2
    expected_list = ["PC (0)", "Mac (1)"]

    assert (
            expected_count == len(list_of_desktops)
    ), f"Expected number of desktops options  {expected_count}, but got {len(list_of_desktops)}"
    assert (
            expected_list == list_of_desktops
    ), f"Expected text {expected_list}, but got {list_of_desktops}"


def test_desktops_pc_count(browser, element_helper):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.click_category("PC")
    ps_count = desktops_page.get_count_of_subcategory("- PC")
    text = element_helper.get_text_for_locator(browser, desktops_page.EMPTY_CONTENT)

    match = re.search(r'\((\d+)\)', ps_count)

    count_of_pc = None
    if match:
        count_of_pc = int(match.group(1))
        print(f'Extracted digit: {count_of_pc}')
    else:
        print('No digit found in parentheses!')

    expected_count = 0
    expected_text = 'There are no products to list in this category.'
    assert (
            expected_count == count_of_pc
    ), f"Expected number of pc  {expected_count}, but got {count_of_pc}"
    assert (
            expected_text == text
    ), f"Expected text {expected_text}, but got {text}"


#TODO: Bug 2
def test_desktops_count_of_elements(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    list_of_desktops = desktops_page.get_list_of_desktops()
    total_count_of_desktops = 0
    for li in list_of_desktops:
        match = int(re.search(r'\((\d+)\)', li).group(1))
        total_count_of_desktops += match

    total_items = desktops_page.get_total_elements_on_page()

    assert (
            total_count_of_desktops == total_items
    ), f"Expected number of items  {total_count_of_desktops}, but got {total_items}"


#TODO: Bug 3
def test_desktops_count_of_categories(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    list_of_desktops = desktops_page.get_list_of_desktops()
    total_count_of_desktops = 0
    for li in list_of_desktops:
        match = int(re.search(r'\((\d+)\)', li).group(1))
        total_count_of_desktops += match

    total_items = desktops_page.get_total_elements_for_category()

    assert (
            total_count_of_desktops == total_items
    ), f"Expected number of items  {total_count_of_desktops}, but got {total_items}"


def test_desktops_sorting(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.sort_by_price_high_to_low()
    list_of_prices_float = desktops_page.get_prices()

    assert list_of_prices_float == sorted(list_of_prices_float, reverse=True), \
        f"Prices are not in descending order: {list_of_prices_float}"


@pytest.mark.parametrize("view_mode, expected_classes", [
    ("list", ["product-list", "row-cols-1", "product-list"]),
    ("grid", ["row-cols-sm-2", "row-cols-md-2", "row-cols-lg-3"])
])
def test_product_view_toggle(browser, view_mode, expected_classes):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")

    desktops_page.click_list_grid_view(view_mode)
    product_list_element = browser.find_element(By.ID, desktops_page.PRODUCT_LIST)

    class_attribute = product_list_element.get_attribute("class")
    print(f"Class attribute of product list in {view_mode} view: {class_attribute}")

    for expected_class in expected_classes:
        assert expected_class in class_attribute, \
            f"Expected '{expected_class}' not found in class attribute for {view_mode} view!"


@pytest.mark.parametrize("currency", [
    "Euro",
    "Pound Sterling"
])
# 3.4 Проверить, что при переключении валют цены на товары меняются в каталоге
def test_change_currency_in_catalog(browser, currency):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.click_category("Mac")

    price_before = desktops_page.get_price_of_product("iMac")
    panel_page = TopPanelPage(browser)
    new_currency_symbol = panel_page.change_currency(currency)
    price_after = desktops_page.get_price_of_product("iMac")
    assert (price_before != price_after
            ), f"Expected that price after {price_after} doesn't equal price before {price_before}"
    assert (new_currency_symbol in price_after
            ), f"Expected that new currency symbol {new_currency_symbol} is present, but actual price contains {price_after}"
