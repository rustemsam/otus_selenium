import allure
from selenium.common import NoSuchElementException

from src.main.pages.base_page import BasePage


class Currency(BasePage):
    CURRENCY_DROPDOWN = "//span[contains(text(),'Currency')]"
    CURRENT_CURRENCY = "//*[contains(text(),'Currency')]/../strong"
    CURRENCY_OPTION = "//*[contains(text(),'{}')]"

    @allure.step("Get current currency")
    def get_currency(self) -> str:
        try:
            current_currency_element = self.wait_for_element(self.CURRENT_CURRENCY)
            currency = current_currency_element.text
            return currency
        except NoSuchElementException as e:
            self.logger.error(f"Failed to retrieve current currency: {e}")
            return ""

    @allure.step("Change currency to '{currency_name}'")
    def change_currency(self, currency_name: str) -> str:
        try:
            self.wait_for_element(self.CURRENCY_DROPDOWN).click()
            currency_option = self.wait_for_element(self.CURRENCY_OPTION.format(currency_name))
            currency_symbol = self._extract_currency_symbol(currency_option.text)
            currency_option.click()
            self.logger.info(f"Currency changed to '{currency_name}' with symbol '{currency_symbol}'")
            return currency_symbol
        except NoSuchElementException as e:
            self.logger.error(f"Failed to change currency to '{currency_name}': {e}")
            return ""

    def _extract_currency_symbol(self, currency_text: str) -> str:
        return currency_text.split(" ")[0] if currency_text else ""
