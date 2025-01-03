import allure
from selenium.common import TimeoutException

from src.main.pages.base_page import BasePage


class AccountLoginPage(BasePage):
    INPUT_EMAIL_NAME = "//input[@id='input-email']"
    INPUT_PASSWORD_NAME = "//input[@id='input-password']"
    SUBMIT_BUTTON = "//button[@type='submit']"
    ACCOUNT_CONTENT = "//div[@id='content']"

    def __init__(self, browser):
        super().__init__(browser)
        self.go_to_login_page()

    def go_to_login_page(self):
        url = f"{self.browser.base_url}/index.php?route=account/login"
        self.browser.get(url)

    @allure.step("Login to the account with account name '{login}'")
    def login_to_account(self, login: str, password: str) -> None:
        try:
            self.input_value(self.INPUT_EMAIL_NAME, login)
            self.input_value(self.INPUT_PASSWORD_NAME, password)
            self.wait_for_element_to_be_clickable(self.SUBMIT_BUTTON).click()
        except Exception as e:
            self.logger.info(f"Error during retry login: {str(e)}")

    @allure.step("Waiting the account page is loaded")
    def wait_for_account_page_loaded(self, timeout: int = BasePage.DEFAULT_TIMEOUT):
        self.wait_for_new_page_loaded("account&customer_token=", timeout)

    @allure.step("Personal account is opened")
    def personal_account_is_opened(self) -> bool:
        try:
            if "account&customer_token=" in self.browser.current_url:
                return True
            account_header = self.wait_for_element(
                "//h1[contains(text(), 'My Account')]", timeout=2
            )
            return bool(account_header)
        except TimeoutException:
            self.logger.info(
                "Account page did not load or unique account element not found within the expected time."
            )
            return False

    @allure.step("Getting account sections")
    def get_account_sections(self) -> list:
        content = self.wait_for_element(self.ACCOUNT_CONTENT)
        return self.get_items_text(content, tag="h2")
