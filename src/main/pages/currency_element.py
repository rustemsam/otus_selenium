from selenium.common import NoSuchElementException

from src.main.pages.base_page import BasePage


class Currency(BasePage):
    CURRENCY_DROPDOWN = "//span[contains(text(),'Currency')]"
    CURRENT_CURRENCY = "//*[contains(text(),'Currency')]/../strong"
    CURRENCY_OPTION = "//*[contains(text(),'{}')]"

    def get_currency(self) -> str:
        try:
            return self.wait_for_element(self.CURRENT_CURRENCY).text
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve current currency: {e}")
            return ""

    def change_currency(self, currency_name: str) -> str:
        try:
            self.wait_for_element(self.CURRENCY_DROPDOWN).click()
            currency_option = self.wait_for_element(
                self.CURRENCY_OPTION.format(currency_name)
            )
            currency_text = currency_option.text
            currency_symbol = currency_text.split(" ")[0]
            currency_option.click()
            return currency_symbol
        except NoSuchElementException as e:
            print(f"Error when trying to change currency to '{currency_name}': {e}")
            return ""
