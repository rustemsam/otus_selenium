from typing import List

import allure
from selenium.common import NoSuchElementException

from src.main.pages.alert_element import AlertElement
from src.main.pages.base_page import BasePage


class Basket(BasePage):
    BASKET = "//div[@id='header-cart']/div/button[@type='button']"
    ITEMS_IN_BASKET = "//table[@class='table table-striped mb-2']/tbody"

    @allure.step("Getting price from the basket")
    def get_price_from_basket(self) -> float:
        alert_success = AlertElement(self.browser)
        alert_success.wait_until_successful_alert_disappeared()
        try:
            updated_price = self.wait_for_element(self.BASKET).text
            price_value = updated_price.split("$")[-1].strip()
            price_float = float(price_value)
            self.logger.info(f"Retrieved basket price: {price_float}")
            return price_float
        except (NoSuchElementException, ValueError) as e:
            self.logger.warning(f"Error retrieving price from basket: {e}")

    @allure.step("Getting item from basket")
    def get_item_from_basket(self) -> List[str]:
        try:
            alert_success = AlertElement(self.browser)
            alert_success.wait_until_successful_alert_disappeared()
            self.click_using_action(self.BASKET)
            elements = self.wait_for_element(self.ITEMS_IN_BASKET)
            items = self.get_items_text(elements, tag="td")
            self.logger.info(f"Items retrieved from basket: {items}")
            return items
        except NoSuchElementException as e:
            self.logger.warning(f"Error when trying to retrieve items from basket: {e}")
            return []
