import re

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.main.pages.base_page import BasePage


class CatalogPage(BasePage):
    DESKTOP_LIST_CONTAINER = "//h3[contains(text(),'Refine Search')]/following-sibling::div[1]//ul"
    CATEGORY = "//a[@class='list-group-item' and contains(text(),'{}')]"
    ACTIVE_SUBCATEGORY = "//a[contains(text(), '{}')]"
    ITEM_IN_CATALOG = "//a[contains(text(), '{}')]"
    ADD_ITEM_TO_BASKET = "//button[@id='button-cart']"
    ADD_ITEM_TO_WISHLIST = "//button[@class='btn btn-light']/i[@class='fa-solid fa-heart']"
    ADD_ITEM_TO_PRODUCT_COMPARISON = "//button[@class='btn btn-light']/i[@class='fa-solid fa-arrow-right-arrow-left']"
    SORT = "//select[@id='input-sort']"
    QUANTITY = "//input[@type='text' and @name='quantity']"
    PRICE_OPTION_HIGH_LOW = "//select[@id='input-sort']/option[contains(text(),'Price (High > Low)')]"
    PRICE_ELEMENTS = "//div[@class='price']"
    SUCCESSFULLY_ALERT = "//div[@class='alert alert-success alert-dismissible']"
    PRICE_IN_CATALOG = "//h2/span[@class='price-new']"
    TOTAL_ELEMENTS_FOR_CATEGORY = "//div/a[@class='list-group-item active']"
    EMPTY_CONTENT = "//*[@id='content']/p"
    TOTAL_ELEMENTS_ON_PAGE = "//div[@class='col-sm-6 text-end']"
    LIST_VIEW = "//button[@id='button-list']"
    GRID_VIEW = "//button[@id='button-grid']"
    PRODUCT_LIST = "product-list"

    def __init__(self, browser):
        super().__init__(browser)

    def get_list_of_desktops(self) -> list:
        try:
            desktops_search_count = self.wait_helper.wait_for_element(self.browser, self.DESKTOP_LIST_CONTAINER)
            return self.element_helper.get_list_items_texts(desktops_search_count)
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve desktops: {e}")
            return []

    def get_count_of_subcategory(self, subcategory: str) -> str:
        try:
            return self.wait_helper.wait_for_element(self.browser, self.ACTIVE_SUBCATEGORY
                                                     .format(subcategory)).text
        except NoSuchElementException:
            print(f"Error when trying to retrieve subcategory : {subcategory}")
            return ""

    def click_category(self, category: str) -> None:
        try:
            self.wait_helper.wait_for_element(self.browser, self.CATEGORY.format(category)).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click category: {e}")

    def click_list_grid_view(self, view_mode: str) -> None:
        if view_mode == "list":
            self.wait_helper.wait_for_element(self.browser, self.LIST_VIEW).click()
        elif view_mode == "grid":
            self.wait_helper.wait_for_element(self.browser, self.GRID_VIEW).click()
        else:
            raise ValueError(f"This view mode  {view_mode} is not defined.")

    def get_total_elements_on_page(self):
        total_elements_on_page = self.element_helper.get_text_for_locator(self.browser, self.TOTAL_ELEMENTS_ON_PAGE)
        match = re.search(r'of\s+(\d+)', total_elements_on_page)
        return int(match.group(1))

    def get_total_elements_for_category(self) -> int:
        total_elements_for_categories = self.element_helper.get_text_for_locator(self.browser,
                                                                                 self.TOTAL_ELEMENTS_FOR_CATEGORY)
        match = re.search(r'\((\d+)\)', total_elements_for_categories)
        if match:
            return int(match.group(1))
        else:
            raise ValueError("Could not find the total elements in the category string.")

    def sort_by_price_high_to_low(self) -> None:
        try:
            self.wait_helper.wait_for_element(self.browser, self.SORT).click()
            self.wait_helper.wait_for_element(self.browser, self.PRICE_OPTION_HIGH_LOW).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click sorting: {e}")

    def get_prices(self) -> list:
        list_of_prices = self.browser.find_elements(By.XPATH, self.PRICE_ELEMENTS)
        list_of_prices_float = []
        for price_element in list_of_prices:
            price_text = price_element.text.strip().split("\n")[0]
            price_cleaned = price_text.replace("$", "").replace(",", "")
            try:
                list_of_prices_float.append(float(price_cleaned))
            except ValueError:
                print(f"Could not convert price: {price_text}")
        return list_of_prices_float

    def click_on_product_item(self, item: str) -> None:
        element = self.wait_helper.wait_for_element_to_be_clickable(self.browser, self.ITEM_IN_CATALOG.format(item))
        self.browser.execute_script("arguments[0].click();", element)

    def get_product_item_price(self) -> str:
        try:
            return self.browser.find_element(By.XPATH, self.PRICE_IN_CATALOG).text
        except NoSuchElementException:
            raise ValueError("Price element for the product item was not found.")

    def get_product_item_price_number(self) -> float:
        price_with_currency = self.get_product_item_price()
        try:
            return float(price_with_currency.replace("$", "").replace(",", ""))
        except ValueError:
            raise ValueError(f"Could not convert price '{price_with_currency}' to a number.")

    def get_successfully_text_alert(self) -> str:
        return self.wait_helper.wait_for_element_to_be_clickable(self.browser, self.SUCCESSFULLY_ALERT).text

    def add_item_to_card(self) -> None:
        try:
            self.wait_helper.wait_for_element(self.browser, self.ADD_ITEM_TO_BASKET).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click add item: {e}")


def add_item_to_wishlist(self) -> None:
    try:
        self.wait_helper.wait_for_element(self.browser, self.ADD_ITEM_TO_WISHLIST).click()
    except NoSuchElementException as e:
        print(f"Error when trying to click add item: {e}")


def add_item_to_product_comparison(self) -> None:
    try:
        self.wait_helper.wait_for_element(self.browser, self.ADD_ITEM_TO_PRODUCT_COMPARISON).click()
    except NoSuchElementException as e:
        print(f"Error when trying to click add item: {e}")


def change_quantity_to(self, quantity: int) -> None:
    try:
        input_field = self.wait_helper.wait_for_element(self.browser, self.QUANTITY)
        input_field.clear()
        input_field.send_keys(quantity)
    except NoSuchElementException as e:
        print(f"Error when trying to fill quantity: {e}")
