from selenium.webdriver.common.by import By

from src.main.models.login_model import AccountRequestBody
from src.main.pages.base_page import BasePage


class AccountRegisterPage(BasePage):
    INPUT_FIRST_NAME = "//input[@id='input-firstname']"
    INPUT_LAST_NAME = "//input[@id='input-lastname']"
    INPUT_EMAIL = "//input[@id='input-email']"
    INPUT_PASSWORD = "//input[@id='input-password']"
    FIRST_NAME_VALIDATION = "//div[@id='error-firstname']"
    LAST_NAME_VALIDATION = "//div[@id='error-lastname']"
    EMAIL_VALIDATION = "//div[@id='error-email']"
    PASSWORD_VALIDATION = "//div[@id='error-password']"
    BOTTOM_XPATH = "window.scrollTo(0, document.body.scrollHeight);"
    AGREE_CHECKBOX = "//input[@name='agree']"
    SUBMIT_BUTTON = "//button[@type='submit']"
    EMAIL = "email"
    JS_VALIDATION_MESSAGE = "return arguments[0].validationMessage;"
    SUCCESSFUL_REGISTRATION = "//div[@id='common-success']/div/div/h1"

    def __init__(self, browser):
        super().__init__(browser)
        self.go_to_register_page()

    def go_to_register_page(self):
        url = f"{self.browser.base_url}/index.php?route=account/register"
        self.browser.get(url)

    def create_user(
        self, account_request_body: AccountRequestBody, agree_checkbox: bool = "true"
    ) -> AccountRequestBody:
        self.input_value(self.INPUT_FIRST_NAME, account_request_body.first_name)
        self.input_value(self.INPUT_LAST_NAME, account_request_body.last_name)
        self.input_value(self.INPUT_EMAIL, account_request_body.email)
        self.input_value(self.INPUT_PASSWORD, account_request_body.password)

        if agree_checkbox:
            agree_checkbox = self.wait_for_element(self.AGREE_CHECKBOX)
            self.js_click_to_element(agree_checkbox)

        submit_button = self.wait_for_element_to_be_clickable(self.SUBMIT_BUTTON)
        self.js_click_to_element(submit_button)

        return account_request_body

    def get_validation_error(self, field_name: str) -> str:
        validation_xpath = {
            "first_name": self.FIRST_NAME_VALIDATION,
            "last_name": self.LAST_NAME_VALIDATION,
            "email": self.EMAIL_VALIDATION,
            "password": self.PASSWORD_VALIDATION,
        }.get(field_name)

        return self.wait_for_element(validation_xpath).text if validation_xpath else ""

    def get_successful_registration_message(self) -> str:
        return self.wait_for_element(self.SUCCESSFUL_REGISTRATION).text

    def get_pop_up_email_validation_error(self) -> str:
        email_field = self.browser.find_element(By.NAME, self.EMAIL)
        return self.browser.execute_script(self.JS_VALIDATION_MESSAGE, email_field)
