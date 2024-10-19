import pytest

from src.main.pages.home_page import HomePage


def test_check_the_price(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.click_category("Mac")
    price_on_catalog = home_page.get_price_of_product("iMac")

    desktops_page.click_on_product_item("iMac")
    price = desktops_page.get_product_item_price()

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
def test_alert_message(browser, type, expected_text):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.click_category("Mac")
    desktops_page.click_on_product_item("iMac")

    if type == "card":
        desktops_page.add_item_to_card()
    elif type == "wishlist":
        desktops_page.add_item_to_wishlist()
    elif type == "comparison":
        desktops_page.add_item_to_product_comparison()

    text = desktops_page.get_successfully_text_alert()
    expected_text = expected_text
    assert expected_text == text, f"Expected text {expected_text}, but got {text}"


def test_add_few_items_to_cart(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.click_category("Mac")
    desktops_page.click_on_product_item("iMac")
    price_cleaned = desktops_page.get_product_item_price_number()

    quantity = 2
    desktops_page.change_quantity_to(quantity)
    desktops_page.add_item_to_card()
    expected_price = quantity * price_cleaned
    price_value = desktops_page.get_price_from_basket()
    updated_price_in_card = price_value
    assert (
        expected_price == updated_price_in_card
    ), f"Expected price for the item is {expected_price}, but got {price_value}"


# TODO Bug 4
def test_add_wrong_item_to_cart(browser):
    home_page = HomePage(browser)
    desktops_page = home_page.go_to_page("Desktops")
    desktops_page.click_category("Mac")
    desktops_page.click_on_product_item("iMac")

    desktops_page.change_quantity_to("wrong")
    desktops_page.add_item_to_card()

    text = desktops_page.get_text_from_failure_alert()
    expected_text = "Failure, please use digits to add count"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"
