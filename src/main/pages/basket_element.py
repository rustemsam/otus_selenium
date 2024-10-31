from selenium.common import NoSuchElementException

from src.main.pages.alert_element import AlertElement
from src.main.pages.base_page import BasePage


class Basket(BasePage):
    BASKET = "//div[@id='header-cart']/div/button[@type='button']"
    ITEMS_IN_BASKET = "//table[@class='table table-striped mb-2']/tbody"

    def get_price_from_basket(self) -> float:
        alert_success = AlertElement(self.browser)
        alert_success.wait_until_successful_alert_disappeared()
        try:
            updated_price = self.wait_for_element(self.BASKET).text
            price_value = updated_price.split("$")[-1].strip()
            return float(price_value)
        except (NoSuchElementException, ValueError) as e:
            print(f"Error retrieving price from basket: {e}")
            return 0.0

    def get_item_from_basket(self) -> list:
        try:
            alert_success = AlertElement(self.browser)
            alert_success.wait_until_successful_alert_disappeared()
            self.click_using_action(self.BASKET)
            elements = self.wait_for_element(self.ITEMS_IN_BASKET)
            return self.get_items_text(elements, tag="td")
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve items from basket: {e}")
            return []
