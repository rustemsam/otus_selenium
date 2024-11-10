import allure
import pytest

from src.main.pages.alert_element import AlertElement
from src.main.pages.basket_element import Basket
from src.main.pages.catalog.catalog_page import CatalogPage
from src.main.pages.home_page import HomePage


@allure.title("Check the price of the them in catalog and product page")
def test_check_the_price(browser):
    home_page = HomePage(browser)
    home_page.go_to_page("Desktops")
    catalog_page = CatalogPage(browser)
    catalog_page.click_category("Mac")
    price_on_catalog = home_page.get_price_of_product("iMac")

    catalog_page.click_on_product_item("iMac")
    price = catalog_page.get_product_item_price()

    assert (
        price_on_catalog == price
    ), f"Expected price {price_on_catalog}, but got {price}"


@pytest.mark.parametrize(
    "button, expected_text",
    [
        ("card", "Success: You have added iMac to your shopping cart!"),
        (
            "wishlist",
            "You must login or create an account to save iMac to your wish list!",
        ),
        ("comparison", "Success: You have added iMac to your product comparison!"),
    ],
)
@allure.title("Check the alert message")
def test_alert_message(browser, button, expected_text):
    home_page = HomePage(browser)
    home_page.go_to_page("Desktops")
    catalog_page = CatalogPage(browser)
    (
        (catalog_page.click_category("Mac").click_on_product_item("iMac")).add_item_to(
            button
        )
    )

    alert_element = AlertElement(browser)
    text = alert_element.get_successfully_text_alert()
    expected_text = expected_text
    assert expected_text == text, f"Expected text {expected_text}, but got {text}"


@allure.title("Check the price in the button cart when adding few items")
def test_add_few_items_to_cart(browser):
    home_page = HomePage(browser)
    home_page.go_to_page("Desktops")
    catalog_page = CatalogPage(browser)
    (catalog_page.click_category("Mac").click_on_product_item("iMac"))
    price_cleaned = catalog_page.get_product_item_price_number()
    basket = Basket(browser)
    quantity = 2
    catalog_page.change_quantity_to(quantity)
    catalog_page.add_item_to("card")
    expected_price = quantity * price_cleaned
    price_value = basket.get_price_from_basket()
    updated_price_in_card = price_value
    assert (
        expected_price == updated_price_in_card
    ), f"Expected price for the item is {expected_price}, but got {price_value}"


# TODO Bug 4
@allure.title("Check the validation for the field quantity")
def test_add_wrong_item_to_cart(browser):
    home_page = HomePage(browser)
    home_page.go_to_page("Desktops")
    catalog_page = CatalogPage(browser)
    (
        (
            catalog_page.click_category("Mac").click_on_product_item("iMac")
        ).change_quantity_to("wrong")
    )
    catalog_page.add_item_to("card")
    alert = AlertElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "Failure, please use digits to add count"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"
