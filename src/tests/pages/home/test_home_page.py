import allure
import pytest

from src.main.pages.basket_element import Basket
from src.main.pages.bottom_panel_element import BottomPanel
from src.main.pages.home_page import HomePage
from src.main.pages.currency_element import Currency


@allure.title("Check the main page title")
def test_main_page_title(browser):
    HomePage(browser)
    expected_title = "Your Store"
    assert (
        expected_title in browser.title
    ), f"Expected title  {expected_title}, but got {browser.title}"


@allure.title("Check the options for the section Information")
def test_information_section(browser):
    HomePage(browser)
    bottom_panel = BottomPanel(browser)
    list_of_elements = bottom_panel.get_bottom_panel_options("Information")

    expected_list = [
        "Terms & Conditions",
        "Delivery Information",
        "About Us",
        "Privacy Policy",
    ]

    assert (
        expected_list == list_of_elements
    ), f"Expected list of elements  {expected_list}, but got {list_of_elements}"


@allure.title("Check the categories section")
def test_categories_section(browser):
    home_page = HomePage(browser)
    categories = home_page.get_list_categories()

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


@allure.title("Check the number of featured items on the main page")
def test_featured(browser):
    home_page = HomePage(browser)
    featured_elements = home_page.get_items_on_featured()

    expected_number_of_elements = 4
    assert (
        expected_number_of_elements == len(featured_elements)
    ), f"Expected length of elements {expected_number_of_elements}, actual {len(featured_elements)}"


@allure.title("Check the default currency on the main page")
def test_default_currency(browser):
    HomePage(browser)
    top_panel = Currency(browser)
    current_currency = top_panel.get_currency()

    expected_default_currency = "$"
    assert (
        expected_default_currency == current_currency
    ), f"Expected currency {expected_default_currency}, actual {current_currency}"


@pytest.mark.parametrize(
    "item",
    [("MacBook"), ("Canon EOS 5D")],
)
@allure.title("Check that the random item from the main page was added to the basket")
# 3.2 Добавить в корзину случайный товар с главной страницы и проверить что он появился в корзине
def test_add_random_item_to_basket(browser, item):
    home_page = HomePage(browser)
    basket = Basket(browser)
    home_page.add_item_to_basket(item)
    product_item = basket.get_item_from_basket()
    expected_count = "x 1"
    assert (
        expected_count in product_item
    ), f"Expected that list contain {expected_count}, actual but the list contains {list}"
    assert any(
        item in item_product for item_product in product_item
    ), f"Expected that list contain {item}, actual but the list contains {list}"


@pytest.mark.parametrize("currency", [("Euro"), ("Pound Sterling")])
# 3.3  Проверить, что при переключении валют цены на товары меняются на главной
@allure.title(
    "Check that when currency is changed the price is changing accordingly on the main page"
)
def test_change_currency(browser, currency):
    home_page = HomePage(browser)
    top_panel = Currency(browser)
    price_before = home_page.get_price_of_product("MacBook")
    new_currency_symbol = top_panel.change_currency(currency)
    price_after = home_page.get_price_of_product("MacBook")

    assert (
        price_before != price_after
    ), f"Expected that price after {price_after} doesn't equal price before {price_before}"
    assert (
        new_currency_symbol in price_after
    ), f"Expected that new currency symbol {new_currency_symbol} is present, but actual price contains {price_after}"
