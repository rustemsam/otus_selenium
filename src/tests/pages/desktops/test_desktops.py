import re

import pytest
from selenium.webdriver.common.by import By

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper
from src.main.pages.top_panel_page import TopPanelPage

MENU = "//*[contains(text(),'{}')]"
SHOW_ALL = "//*[contains(text(),'Show All {}')]"
PRODUCT_PRICE = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//span[@class='price-new']"
DESKTOP_LIST_CONTAINER = (
    "//h3[contains(text(),'Refine Search')]/following-sibling::div[1]//ul"
)
CATEGORY = "//a[@class='list-group-item' and contains(text(),'{}')]"
ACTIVE_SUBCATEGORY = "//a[contains(text(), '{}')]"
SORT = "//select[@id='input-sort']"
PRICE_OPTION_HIGH_LOW = (
    "//select[@id='input-sort']/option[contains(text(),'Price (High > Low)')]"
)
PRICE_ELEMENTS = "//div[@class='price']"
TOTAL_ELEMENTS_FOR_CATEGORY = "//div/a[@class='list-group-item active']"
EMPTY_CONTENT = "//*[@id='content']/p"
TOTAL_ELEMENTS_ON_PAGE = "//div[@class='col-sm-6 text-end']"
LIST_VIEW = "//button[@id='button-list']"
GRID_VIEW = "//button[@id='button-grid']"
PRODUCT_LIST = "product-list"


@pytest.fixture(scope="session")
def wait_helper():
    return WaitHelper()


@pytest.fixture(scope="session")
def element_helper():
    return ElementHelper()


@pytest.fixture(autouse=True)
def run_around_tests(browser):
    browser.get(browser.base_url)


def test_desktops(browser, wait_helper, element_helper):
    go_to_page(browser, wait_helper, "Desktops")
    list_of_desktops = get_list_of_desktops(browser, wait_helper, element_helper)

    expected_count = 2
    expected_list = ["PC (0)", "Mac (1)"]

    assert (
        expected_count == len(list_of_desktops)
    ), f"Expected number of desktops options  {expected_count}, but got {len(list_of_desktops)}"
    assert (
        expected_list == list_of_desktops
    ), f"Expected text {expected_list}, but got {list_of_desktops}"


def test_desktops_pc_count(browser, wait_helper, element_helper):
    go_to_page(browser, wait_helper, "Desktops")
    click_category(browser, wait_helper, "PC")
    ps_count = get_count_of_subcategory(browser, wait_helper, "- PC")
    text = element_helper.get_text_for_locator(browser, EMPTY_CONTENT)

    match = re.search(r"\((\d+)\)", ps_count)

    count_of_pc = None
    if match:
        count_of_pc = int(match.group(1))
        print(f"Extracted digit: {count_of_pc}")
    else:
        print("No digit found in parentheses!")

    expected_count = 0
    expected_text = "There are no products to list in this category."
    assert (
        expected_count == count_of_pc
    ), f"Expected number of pc  {expected_count}, but got {count_of_pc}"
    assert expected_text == text, f"Expected text {expected_text}, but got {text}"


# TODO: Bug 2
def test_desktops_count_of_elements(browser, wait_helper, element_helper):
    go_to_page(browser, wait_helper, "Desktops")
    list_of_desktops = get_list_of_desktops(browser, wait_helper, element_helper)

    total_count_of_desktops = 0
    for li in list_of_desktops:
        match = int(re.search(r"\((\d+)\)", li).group(1))
        total_count_of_desktops += match

    total_items = get_total_elements_on_page(browser, element_helper)

    assert (
        total_count_of_desktops == total_items
    ), f"Expected number of items  {total_count_of_desktops}, but got {total_items}"


# TODO: Bug 3
def test_desktops_count_of_categories(browser, wait_helper, element_helper):
    go_to_page(browser, wait_helper, "Desktops")
    list_of_desktops = get_list_of_desktops(browser, wait_helper, element_helper)
    total_count_of_desktops = 0
    for li in list_of_desktops:
        match = int(re.search(r"\((\d+)\)", li).group(1))
        total_count_of_desktops += match

    total_items = get_total_elements_for_category(browser, element_helper)

    assert (
        total_count_of_desktops == total_items
    ), f"Expected number of items  {total_count_of_desktops}, but got {total_items}"


def test_desktops_sorting(browser, wait_helper):
    go_to_page(browser, wait_helper, "Desktops")
    sort_by_price_high_to_low(browser, wait_helper)
    list_of_prices_float = get_prices(browser)

    assert list_of_prices_float == sorted(
        list_of_prices_float, reverse=True
    ), f"Prices are not in descending order: {list_of_prices_float}"


@pytest.mark.parametrize(
    "view_mode, expected_classes",
    [
        ("list", ["product-list", "row-cols-1", "product-list"]),
        ("grid", ["row-cols-sm-2", "row-cols-md-2", "row-cols-lg-3"]),
    ],
)
def test_product_view_toggle(browser, wait_helper, view_mode, expected_classes):
    go_to_page(browser, wait_helper, "Desktops")

    click_list_grid_view(browser, wait_helper, view_mode)
    product_list_element = browser.find_element(By.ID, PRODUCT_LIST)

    class_attribute = product_list_element.get_attribute("class")
    print(f"Class attribute of product list in {view_mode} view: {class_attribute}")

    for expected_class in expected_classes:
        assert (
            expected_class in class_attribute
        ), f"Expected '{expected_class}' not found in class attribute for {view_mode} view!"


@pytest.mark.parametrize("currency", ["Euro", "Pound Sterling"])
# 3.4 Проверить, что при переключении валют цены на товары меняются в каталоге
def test_change_currency_in_catalog(browser, wait_helper, currency):
    go_to_page(browser, wait_helper, "Desktops")
    click_category(browser, wait_helper, "Mac")

    price_before = get_price_of_product(browser, wait_helper, "iMac")
    panel_page = TopPanelPage(browser)
    new_currency_symbol = panel_page.change_currency(currency)
    price_after = get_price_of_product(browser, wait_helper, "iMac")
    assert (
        price_before != price_after
    ), f"Expected that price after {price_after} doesn't equal price before {price_before}"
    assert (
        new_currency_symbol in price_after
    ), f"Expected that new currency symbol {new_currency_symbol} is present, but actual price contains {price_after}"


def go_to_page(browser, wait_helper, menu_item: str):
    wait_helper.wait_for_element(browser, MENU.format(menu_item)).click()
    wait_helper.wait_for_element(browser, SHOW_ALL.format(menu_item)).click()


def get_list_of_desktops(browser, wait_helper, element_helper) -> list:
    desktops_search_count = wait_helper.wait_for_element(
        browser, DESKTOP_LIST_CONTAINER
    )
    return element_helper.get_list_items_texts(desktops_search_count)


def click_category(browser, wait_helper, category: str) -> None:
    wait_helper.wait_for_element(browser, CATEGORY.format(category)).click()


def get_count_of_subcategory(browser, wait_helper, subcategory: str) -> str:
    return wait_helper.wait_for_element(
        browser, ACTIVE_SUBCATEGORY.format(subcategory)
    ).text


def get_total_elements_on_page(browser, element_helper):
    total_elements_on_page = element_helper.get_text_for_locator(
        browser, TOTAL_ELEMENTS_ON_PAGE
    )
    match = re.search(r"of\s+(\d+)", total_elements_on_page)
    return int(match.group(1))


def get_total_elements_for_category(browser, element_helper) -> int:
    total_elements_for_categories = element_helper.get_text_for_locator(
        browser, TOTAL_ELEMENTS_FOR_CATEGORY
    )
    match = re.search(r"\((\d+)\)", total_elements_for_categories)
    if match:
        return int(match.group(1))
    else:
        raise ValueError("Could not find the total elements in the category string.")


def sort_by_price_high_to_low(browser, wait_helper) -> None:
    wait_helper.wait_for_element(browser, SORT).click()
    wait_helper.wait_for_element(browser, PRICE_OPTION_HIGH_LOW).click()


def get_prices(browser) -> list:
    list_of_prices = browser.find_elements(By.XPATH, PRICE_ELEMENTS)
    list_of_prices_float = []
    for price_element in list_of_prices:
        price_text = price_element.text.strip().split("\n")[0]
        price_cleaned = price_text.replace("$", "").replace(",", "")
        try:
            list_of_prices_float.append(float(price_cleaned))
        except ValueError:
            print(f"Could not convert price: {price_text}")
    return list_of_prices_float


def click_list_grid_view(browser, wait_helper, view_mode: str) -> None:
    if view_mode == "list":
        wait_helper.wait_for_element(browser, LIST_VIEW).click()
    elif view_mode == "grid":
        wait_helper.wait_for_element(browser, GRID_VIEW).click()
    else:
        raise ValueError(f"This view mode  {view_mode} is not defined.")


def get_price_of_product(browser, wait_helper, product_name: str) -> str:
    return wait_helper.wait_for_element(
        browser, PRODUCT_PRICE.format(product_name)
    ).text
