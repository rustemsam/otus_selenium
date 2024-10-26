import pytest
from selenium.webdriver.common.by import By

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper

BOTTOM_PANEL = "//div/*[contains(text(),'{}')]/../ul"
CATEGORIES = "//ul[@class='nav navbar-nav']"
FEATURED_ITEMS = "//*[contains(text(),'Featured')]/../div[2]"
ITEM_TO_CARD = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//button[@title='Add to Cart']"
JS_ARGUMENT_CLICK = "arguments[0].click();"
BASKET = "//div[@class='dropdown d-grid']"
ITEMS_IN_BASKET = "//table[@class='table table-striped mb-2']/tbody"
PRODUCT_PRICE = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//span[@class='price-new']"
CURRENCY_DROPDOWN = "//span[contains(text(),'Currency')]"
CURRENT_CURRENCY = "//*[contains(text(),'Currency')]/../strong"
CURRENCY_OPTION = "//*[contains(text(),'{}')]"
SUCCESS_ALERT = "//div[@class='alert alert-success alert-dismissible']"


@pytest.fixture(scope="session")
def wait_helper():
    return WaitHelper()


@pytest.fixture(scope="session")
def element_helper():
    return ElementHelper()


@pytest.fixture(autouse=True)
def run_around_tests(browser):
    browser.get(browser.base_url)


def test_main_page_title(browser):
    browser.get(browser.base_url)
    expected_title = "Your Store"
    assert (
        expected_title in browser.title
    ), f"Expected title  {expected_title}, but got {browser.title}"


def test_information_section(browser, wait_helper, element_helper):
    list_of_elements = get_options_for(
        browser, wait_helper, element_helper, "Information"
    )

    expected_list = [
        "Terms & Conditions",
        "Delivery Information",
        "About Us",
        "Privacy Policy",
    ]

    assert (
        expected_list == list_of_elements
    ), f"Expected list of elements  {expected_list}, but got {list_of_elements}"


def test_categories_section(browser, wait_helper, element_helper):
    categories = get_list_categories(browser, wait_helper, element_helper)

    expected_list = [
        "Desktops",
        "Laptops & Notebooks",
        "Components",
        "Tablets",
        "Software",
        "Phones & PDAs",
        "Cameras",
        "MP3 Players",
    ]
    assert (
        expected_list == categories
    ), f"Expected list of elements  {expected_list}, but got {categories}"


def test_featured(browser, wait_helper):
    featured_elements = get_items_on_featured(browser, wait_helper)

    expected_number_of_elements = 4
    assert (
        expected_number_of_elements == len(featured_elements)
    ), f"Expected length of elements {expected_number_of_elements}, actual {len(featured_elements)}"


def test_default_currency(browser, wait_helper):
    current_currency = get_currency(browser, wait_helper)

    expected_default_currency = "$"
    assert (
        expected_default_currency == current_currency
    ), f"Expected currency {expected_default_currency}, actual {current_currency}"


@pytest.mark.parametrize(
    "item",
    [
        ("MacBook"),
        # ("Canon EOS 5D") TODO Bug: 1
    ],
)
# 3.2 Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине
def test_add_random_item_to_basket(browser, wait_helper, element_helper, item):
    add_item_to_basket(browser, wait_helper, item)
    product_item = get_item_from_basket(browser, wait_helper, element_helper)
    expected_count = "x 1"
    assert (
        expected_count in product_item
    ), f"Expected that list contain {expected_count}, actual but the list contains {list}"
    assert any(
        item in item_product for item_product in product_item
    ), f"Expected that list contain {item}, actual but the list contains {list}"


@pytest.mark.parametrize("currency", [("Euro"), ("Pound Sterling")])
# 3.3  Проверить, что при переключении валют цены на товары меняются на главной
def test_change_currency(browser, wait_helper, currency):
    price_before = get_price_of_product(browser, wait_helper, "MacBook")
    new_currency_symbol = change_currency(browser, wait_helper, currency)
    price_after = get_price_of_product(browser, wait_helper, "MacBook")

    assert (
        price_before != price_after
    ), f"Expected that price after {price_after} doesn't equal price before {price_before}"
    assert (
        new_currency_symbol in price_after
    ), f"Expected that new currency symbol {new_currency_symbol} is present, but actual price contains {price_after}"


def get_options_for(browser, wait_helper, element_helper, option: str) -> list:
    ul_element = wait_helper.wait_for_element(browser, BOTTOM_PANEL.format(option))
    return element_helper.get_list_items_texts(ul_element)


def get_list_categories(browser, wait_helper, element_helper) -> list:
    categories = wait_helper.wait_for_element(browser, CATEGORIES)
    return element_helper.get_list_items_texts(categories)


def get_items_on_featured(browser, wait_helper) -> list:
    element = wait_helper.wait_for_element(browser, FEATURED_ITEMS)
    return element.find_elements(By.XPATH, "div")


def get_currency(browser, wait_helper) -> str:
    return wait_helper.wait_for_element(browser, CURRENT_CURRENCY).text


def change_currency(browser, wait_helper, currency_name: str) -> str:
    wait_helper.wait_for_element(browser, CURRENCY_DROPDOWN).click()
    currency_option = wait_helper.wait_for_element(
        browser, CURRENCY_OPTION.format(currency_name)
    )
    currency_text = currency_option.text
    currency_symbol = currency_text.split(" ")[0]
    currency_option.click()
    return currency_symbol


def add_item_to_basket(browser, wait_helper, item: str) -> None:
    element = wait_helper.wait_for_element(browser, ITEM_TO_CARD.format(item))
    browser.execute_script(JS_ARGUMENT_CLICK, element)
    wait_until_successful_alert_disappeared(browser, wait_helper)


def wait_until_successful_alert_disappeared(browser, wait_helper) -> None:
    wait_helper.wait_for_element_to_disappear(browser, SUCCESS_ALERT)


def get_item_from_basket(browser, wait_helper, element_helper) -> list:
    wait_helper.wait_for_element(browser, BASKET).click()
    elements = wait_helper.wait_for_element(browser, ITEMS_IN_BASKET)
    return element_helper.get_list_items_texts(elements, tag="td")


def get_price_of_product(browser, wait_helper, product_name: str) -> str:
    return wait_helper.wait_for_element(
        browser, PRODUCT_PRICE.format(product_name)
    ).text
