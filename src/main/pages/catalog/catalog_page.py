import re

import allure
from selenium.common import (
    NoSuchElementException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from src.main.pages.base_page import BasePage


class CatalogPage(BasePage):
    DESKTOP_LIST_CONTAINER = (
        "//h3[contains(text(),'Refine Search')]/following-sibling::div[1]//ul"
    )
    CATEGORY = "//a[@class='list-group-item' and contains(text(),'{}')]"
    ACTIVE_SUBCATEGORY = "//a[contains(text(), '{}')]"
    ITEM_IN_CATALOG = "//a[contains(text(), '{}')]"
    ADD_ITEM_TO_BASKET = "//button[@id='button-cart']"
    EMPTY_CART_MESSAGE = "//li[contains(text(), 'Your shopping cart is empty!')]"
    ADD_ITEM_TO_WISHLIST = (
        "//button[@class='btn btn-light']/i[@class='fa-solid fa-heart']"
    )
    ADD_ITEM_TO_PRODUCT_COMPARISON = "//button[@class='btn btn-light']/i[@class='fa-solid fa-arrow-right-arrow-left']"
    SORT = "//select[@id='input-sort']"
    QUANTITY = "//input[@type='text' and @name='quantity']"
    PRICE_OPTION_HIGH_LOW = (
        "//select[@id='input-sort']/option[contains(text(),'Price (High > Low)')]"
    )
    PRICE_ELEMENTS = "//div[@class='price']"
    PRICE_IN_CATALOG = "//h2/span[@class='price-new']"
    TOTAL_ELEMENTS_FOR_CATEGORY = "//div/a[@class='list-group-item active']"
    EMPTY_CONTENT = "//*[@id='content']/p"
    TOTAL_ELEMENTS_ON_PAGE = "//div[@class='col-sm-6 text-end']"
    LIST_VIEW = "//button[@id='button-list']"
    GRID_VIEW = "//button[@id='button-grid']"
    PRODUCT_LIST = "product-list"

    @allure.step("Getting list of desktops ")
    def get_list_of_desktops(self) -> list:
        try:
            desktops_search_count = self.wait_for_element(self.DESKTOP_LIST_CONTAINER)
            return self.get_items_text(desktops_search_count)
        except NoSuchElementException as e:
            self.logger.error(f"Error when trying to retrieve desktops: {e}")
            return []

    @allure.step("Getting count of '{subcategory}'")
    def get_count_of_subcategory(self, subcategory: str) -> str:
        try:
            return self.wait_for_element(
                self.ACTIVE_SUBCATEGORY.format(subcategory)
            ).text
        except NoSuchElementException:
            self.logger.warning(
                f"Error when trying to retrieve subcategory : {subcategory}"
            )
            return ""

    @allure.step("Click '{category}' category")
    def click_category(self, category: str):
        try:
            self.wait_for_element(self.CATEGORY.format(category)).click()
        except NoSuchElementException as e:
            self.logger.error(f"Error when trying to click category: {e}")
        return self

    @allure.step("Switch to '{view_mode}' view mode")
    def click_list_grid_view(self, view_mode: str) -> None:
        if view_mode == "list":
            self.wait_for_element(self.LIST_VIEW).click()
        elif view_mode == "grid":
            self.wait_for_element(self.GRID_VIEW).click()
        else:
            raise ValueError(f"This view mode  {view_mode} is not defined.")

    @allure.step("Getting total elements on page")
    def get_total_elements_on_page(self) -> int:
        total_elements_on_page = self.get_text(self.TOTAL_ELEMENTS_ON_PAGE)
        match = re.search(r"of\s+(\d+)", total_elements_on_page)
        return int(match.group(1)) if match else 0

    @allure.step("Getting total elements for category")
    def get_total_elements_for_category(self) -> int:
        total_elements_for_categories = self.get_text(self.TOTAL_ELEMENTS_FOR_CATEGORY)
        match = re.search(r"\((\d+)\)", total_elements_for_categories)
        return int(match.group(1)) if match else 0

    @allure.step("Sorting items by price: High to Low")
    def sort_by_price_high_to_low(self) -> None:
        try:
            self.wait_for_element(self.SORT).click()
            self.wait_for_element(self.PRICE_OPTION_HIGH_LOW).click()
        except NoSuchElementException as e:
            self.logger.error(f"Error when trying to click sorting: {e}")

    @allure.step("Retrieve all product prices")
    def get_prices(self) -> list:
        prices = self.browser.find_elements(By.XPATH, self.PRICE_ELEMENTS)
        return [
            self._convert_price_to_float(price.text) for price in prices if price.text
        ]

    @allure.step("Click on product '{item}'")
    def click_on_product_item(self, item: str):
        element = self.wait_for_element_to_be_clickable(
            self.ITEM_IN_CATALOG.format(item)
        )
        self.js_click_to_element(element)
        return self

    @allure.step("Retrieve product item price")
    def get_product_item_price(self) -> str:
        try:
            return self.browser.find_element(By.XPATH, self.PRICE_IN_CATALOG).text
        except NoSuchElementException:
            self.logger.error("Price element not found.")
            return ""

    @allure.step("Retrieve numeric price of the product item")
    def get_product_item_price_number(self) -> float:
        price_with_currency = self.get_product_item_price()
        return self._convert_price_to_float(price_with_currency)

    def _convert_price_to_float(self, price_text: str) -> float:
        try:
            return float(price_text.replace("$", "").replace(",", ""))
        except ValueError:
            self.logger.warning(f"Unable to convert price '{price_text}' to float.")
            return 0.0

    @allure.step("Adding item to '{action}'")
    def add_item_to(self, action: str) -> None:
        locators = {
            "card": self.ADD_ITEM_TO_BASKET,
            "wishlist": self.ADD_ITEM_TO_WISHLIST,
            "comparison": self.ADD_ITEM_TO_PRODUCT_COMPARISON,
        }
        locator = locators.get(action)

        if locator:
            try:
                actions = ActionChains(self.browser)
                actions.move_to_element(
                    self.wait_for_element(locator)
                ).click().perform()
                print(f"Item added to {action} successfully.")
            except NoSuchElementException as e:
                self.logger.error(f"Error when trying to add item to {action}: {e}")
        else:
            self.logger.error(
                f"Invalid action: '{action}'. Expected 'basket', 'wishlist', or 'comparison'."
            )

    @allure.step("Changing quantity to '{quantity}'")
    def change_quantity_to(self, quantity: int):
        try:
            input_field = self.wait_for_element(self.QUANTITY)
            input_field.clear()
            input_field.send_keys(quantity)
        except NoSuchElementException as e:
            self.logger.error(f"Error when trying to fill quantity: {e}")
        return self
