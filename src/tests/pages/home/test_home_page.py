import pytest

from src.main.pages.home_page import HomePage


def test_main_page_title(browser):
    browser.get(browser.base_url)
    expected_title = "Your Store"
    assert (
        expected_title in browser.title
    ), f"Expected title  {expected_title}, but got {browser.title}"


def test_information_section(browser):
    home_page = HomePage(browser)
    bottom_panel = home_page.get_panel_page_object("bottom")
    list_of_elements = bottom_panel.get_options_for("Information")

    expected_list = [
        "Terms & Conditions",
        "Delivery Information",
        "About Us",
        "Privacy Policy",
    ]

    assert (
        expected_list == list_of_elements
    ), f"Expected list of elements  {expected_list}, but got {list_of_elements}"


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


def test_featured(browser):
    home_page = HomePage(browser)
    featured_elements = home_page.get_items_on_featured()

    expected_number_of_elements = 4
    assert (
        expected_number_of_elements == len(featured_elements)
    ), f"Expected length of elements {expected_number_of_elements}, actual {len(featured_elements)}"


def test_default_currency(browser):
    home_page = HomePage(browser)
    top_panel_page = home_page.get_panel_page_object("top")
    current_currency = top_panel_page.get_currency()

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
def test_add_random_item_to_basket(browser, item):
    home_page = HomePage(browser)

    home_page.add_item_to_basket(item)
    product_item = home_page.get_item_from_basket()
    expected_count = "x 1"
    assert (
        expected_count in product_item
    ), f"Expected that list contain {expected_count}, actual but the list contains {list}"
    assert any(
        item in item_product for item_product in product_item
    ), f"Expected that list contain {item}, actual but the list contains {list}"


@pytest.mark.parametrize("currency", [("Euro"), ("Pound Sterling")])
# 3.3  Проверить, что при переключении валют цены на товары меняются на главной
def test_change_currency(browser, currency):
    home_page = HomePage(browser)

    price_before = home_page.get_price_of_product("MacBook")
    panel_page = home_page.get_panel_page_object("top")
    new_currency_symbol = panel_page.change_currency(currency)
    price_after = home_page.get_price_of_product("MacBook")

    assert (
        price_before != price_after
    ), f"Expected that price after {price_after} doesn't equal price before {price_before}"
    assert (
        new_currency_symbol in price_after
    ), f"Expected that new currency symbol {new_currency_symbol} is present, but actual price contains {price_after}"
