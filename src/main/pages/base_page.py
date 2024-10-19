from selenium.common import NoSuchElementException

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper


class BasePage:
    SUCCESS_ALERT = "//div[@class='alert alert-success alert-dismissible']"
    FAILURE_ALERT = "//div[@class='alert alert-danger alert-dismissible']"
    BASKET = "//div[@id='header-cart']/div/button[@type='button']"

    def __init__(self, browser):
        self.browser = browser
        self.wait_helper = WaitHelper()
        self.element_helper = ElementHelper()

    def wait_until_successful_alert_disappeared(self) -> None:
        try:
            self.wait_helper.wait_for_element_to_disappear(
                self.browser, self.SUCCESS_ALERT
            )
        except NoSuchElementException:
            print("Success alert not found")

    def get_text_from_failure_alert(self) -> str:
        try:
            return self.wait_helper.wait_for_element(
                self.browser, self.FAILURE_ALERT
            ).text
        except NoSuchElementException:
            print("Failure alert not found.")
            return ""

    def get_price_from_basket(self) -> float:
        self.wait_until_successful_alert_disappeared()
        try:
            updated_price = self.wait_helper.wait_for_element(
                self.browser, self.BASKET
            ).text
            price_value = updated_price.split("$")[-1].strip()
            return float(price_value)
        except (NoSuchElementException, ValueError) as e:
            print(f"Error retrieving price from basket: {e}")
            return 0.0

    def fill_input_field(self, locator: str, value: str) -> None:
        element = self.wait_helper.wait_for_element(self.browser, locator)
        element.clear()
        element.send_keys(value)
