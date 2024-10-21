import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper
from src.tests.pages.home.test_home_page import wait_until_successful_alert_disappeared

MENU = "//*[contains(text(),'{}')]"
SHOW_ALL = "//*[contains(text(),'Show All {}')]"
CATEGORIES = "//ul[@class='nav navbar-nav']"
FEATURED_ITEMS = "//*[contains(text(),'Featured')]/../div[2]"
ITEM_TO_CARD = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//button[@title='Add to Cart']"
JS_ARGUMENT_CLICK = "arguments[0].click();"
BASKET = "//div[@class='dropdown d-grid']"
ITEMS_IN_BASKET = "//table[@class='table table-striped mb-2']/tbody"
PRODUCT_PRICE = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//span[@class='price-new']"
CATEGORY = "//a[@class='list-group-item' and contains(text(),'{}')]"
ITEM_IN_CATALOG = "//a[contains(text(), '{}')]"
PRICE_IN_CATALOG = "//h2/span[@class='price-new']"
ADD_ITEM_TO_BASKET = "//button[@id='button-cart']"
ADD_ITEM_TO_WISHLIST = "//button[@class='btn btn-light']/i[@class='fa-solid fa-heart']"
ADD_ITEM_TO_PRODUCT_COMPARISON = (
    "//button[@class='btn btn-light']/i[@class='fa-solid fa-arrow-right-arrow-left']"
)
SUCCESSFULLY_ALERT = "//div[@class='alert alert-success alert-dismissible']"
QUANTITY = "//input[@type='text' and @name='quantity']"
FAILURE_ALERT = "//div[@class='alert alert-danger alert-dismissible']"


@pytest.fixture(scope="session")
def wait_helper():
    return WaitHelper()


@pytest.fixture(scope="session")
def element_helper():
    return ElementHelper()


@pytest.fixture(autouse=True)
def run_around_tests(browser):
    browser.get(browser.base_url)


def test_check_the_price(browser, wait_helper):
    go_to_page(browser, wait_helper, "Desktops")
    click_category(browser, wait_helper, "Mac")
    price_on_catalog = get_price_of_product(browser, wait_helper, "iMac")

    click_on_product_item(browser, wait_helper, "iMac")
    price = get_product_item_price(browser)

    assert (
        price_on_catalog == price
    ), f"Expected price {price_on_catalog}, but got {price}"


@pytest.mark.parametrize(
    "type, expected_text",
    [
        ("card", "Success: You have added iMac to your shopping cart!"),
        (
            "wishlist",
            "You must login or create an account to save iMac to your wish list!",
        ),
        ("comparison", "Success: You have added iMac to your product comparison!"),
    ],
)
def test_alert_message(browser, wait_helper, type, expected_text):
    go_to_page(browser, wait_helper, "Desktops")
    click_category(browser, wait_helper, "Mac")
    click_on_product_item(browser, wait_helper, "iMac")

    if type == "card":
        add_item_to_card(browser, wait_helper)
    elif type == "wishlist":
        add_item_to_wishlist(browser, wait_helper)
    elif type == "comparison":
        add_item_to_product_comparison(browser, wait_helper)

    text = get_successfully_text_alert(browser, wait_helper)
    expected_text = expected_text
    assert expected_text == text, f"Expected text {expected_text}, but got {text}"


def test_add_few_items_to_cart(browser, wait_helper):
    go_to_page(browser, wait_helper, "Desktops")
    click_category(browser, wait_helper, "Mac")
    click_on_product_item(browser, wait_helper, "iMac")
    price_cleaned = get_product_item_price_number(browser)

    quantity = 2
    change_quantity_to(browser, wait_helper, quantity)
    add_item_to_card(browser, wait_helper)
    expected_price = quantity * price_cleaned
    price_value = get_price_from_basket(browser, wait_helper)
    updated_price_in_card = price_value
    assert (
        expected_price == updated_price_in_card
    ), f"Expected price for the item is {expected_price}, but got {price_value}"


# TODO Bug 4
def test_add_wrong_item_to_cart(browser, wait_helper):
    go_to_page(browser, wait_helper, "Desktops")
    click_category(browser, wait_helper, "Mac")
    click_on_product_item(browser, wait_helper, "iMac")

    change_quantity_to(browser, wait_helper, "wrong")
    add_item_to_card(browser, wait_helper)

    text = get_text_from_failure_alert(browser, wait_helper)
    expected_text = "Failure, please use digits to add count"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


def go_to_page(browser, wait_helper, menu_item: str):
    wait_helper.wait_for_element(browser, MENU.format(menu_item)).click()
    wait_helper.wait_for_element(browser, SHOW_ALL.format(menu_item)).click()


def click_category(browser, wait_helper, category: str) -> None:
    wait_helper.wait_for_element(browser, CATEGORY.format(category)).click()


def get_price_of_product(browser, wait_helper, product_name: str) -> str:
    return wait_helper.wait_for_element(
        browser, PRODUCT_PRICE.format(product_name)
    ).text


def click_on_product_item(browser, wait_helper, item: str) -> None:
    element = wait_helper.wait_for_element_to_be_clickable(
        browser, ITEM_IN_CATALOG.format(item)
    )
    browser.execute_script("arguments[0].click();", element)


def get_product_item_price(browser) -> str:
    return browser.find_element(By.XPATH, PRICE_IN_CATALOG).text


def add_item_to_card(browser, wait_helper) -> None:
    wait_helper.wait_for_element(browser, ADD_ITEM_TO_BASKET).click()


def add_item_to_wishlist(browser, wait_helper) -> None:
    wait_helper.wait_for_element(browser, ADD_ITEM_TO_WISHLIST).click()


def add_item_to_product_comparison(browser, wait_helper) -> None:
    wait_helper.wait_for_element(browser, ADD_ITEM_TO_PRODUCT_COMPARISON).click()


def get_successfully_text_alert(browser, wait_helper) -> str:
    return wait_helper.wait_for_element_to_be_clickable(
        browser, SUCCESSFULLY_ALERT
    ).text


def get_product_item_price_number(browser) -> float:
    price_with_currency = get_product_item_price(browser)
    try:
        return float(price_with_currency.replace("$", "").replace(",", ""))
    except ValueError:
        raise ValueError(
            f"Could not convert price '{price_with_currency}' to a number."
        )


def change_quantity_to(browser, wait_helper, quantity: int) -> None:
    input_field = wait_helper.wait_for_element(browser, QUANTITY)
    input_field.clear()
    input_field.send_keys(quantity)


def get_price_from_basket(browser, wait_helper) -> float:
    wait_until_successful_alert_disappeared(browser, wait_helper)
    try:
        updated_price = wait_helper.wait_for_element(browser, BASKET).text
        price_value = updated_price.split("$")[-1].strip()
        return float(price_value)
    except (NoSuchElementException, ValueError) as e:
        print(f"Error retrieving price from basket: {e}")
        return 0.0


def get_text_from_failure_alert(browser, wait_helper) -> str:
    try:
        return wait_helper.wait_for_element(browser, FAILURE_ALERT).text
    except NoSuchElementException:
        print("Failure alert not found.")
        return ""
