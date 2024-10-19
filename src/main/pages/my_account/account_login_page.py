from selenium.common import TimeoutException

from src.main.pages.base_page import BasePage


class AccountLoginPage(BasePage):
    DEFAULT_TIMEOUT = 10
    ALERT_DANGER = "//div[contains(@class,'alert-danger')]"
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

    def get_text_from_alert_danger(self) -> str:
        return self.wait_helper.wait_for_element(self.browser, self.ALERT_DANGER).text

    def login_to_account(self, login: str, password: str) -> None:
        try:
            self.fill_input_field(self.INPUT_EMAIL_NAME, login)
            self.fill_input_field(self.INPUT_PASSWORD_NAME, password)

            self.wait_helper.wait_for_element_to_be_clickable(
                self.browser, self.SUBMIT_BUTTON
            ).click()
        except Exception as e:
            print(f"Error during retry login: {str(e)}")

    def wait_for_account_page_loaded(self, timeout: int = DEFAULT_TIMEOUT):
        self.wait_helper.wait_for_new_page_loaded(
            self.browser, "account&customer_token=", timeout
        )

    def personal_account_is_opened(self) -> bool:
        try:
            self.wait_for_account_page_loaded(2)
            is_opened = True
        except TimeoutException:
            print("Page did not load correctly after login within the expected time.")
            is_opened = False
        return is_opened

    def get_account_sections(self) -> list:
        content = self.wait_helper.wait_for_element(self.browser, self.ACCOUNT_CONTENT)
        return self.element_helper.get_list_items_texts(content, tag="h2")
