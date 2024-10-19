from selenium.common import NoSuchElementException

from src.main.helper.wait_helper import WaitHelper


class TopPanelPage:
    CURRENCY_DROPDOWN = "//span[contains(text(),'Currency')]"
    CURRENT_CURRENCY = "//*[contains(text(),'Currency')]/../strong"
    CURRENCY_OPTION = "//*[contains(text(),'{}')]"

    def __init__(self, browser):
        self.browser = browser
        self.wait_helper = WaitHelper()

    def get_currency(self) -> str:
        try:
            return self.wait_helper.wait_for_element(
                self.browser, self.CURRENT_CURRENCY
            ).text
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve current currency: {e}")
            return ""

    def change_currency(self, currency_name: str) -> str:
        try:
            self.wait_helper.wait_for_element(
                self.browser, self.CURRENCY_DROPDOWN
            ).click()
            currency_option = self.wait_helper.wait_for_element(
                self.browser, self.CURRENCY_OPTION.format(currency_name)
            )
            currency_text = currency_option.text
            currency_symbol = currency_text.split(" ")[0]
            currency_option.click()
            return currency_symbol
        except NoSuchElementException as e:
            print(f"Error when trying to change currency to '{currency_name}': {e}")
            return ""
