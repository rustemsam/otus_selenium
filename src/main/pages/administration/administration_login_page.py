from selenium.common import NoSuchElementException

from src.main.pages.administration.administration_dashboard_page import (
    AdministrationDashboardPage,
)
from src.main.pages.base_page import BasePage


class AdministrationLoginPage(BasePage):
    ADMIN_CARD_HEADER = "//div[@class='card-header']"
    USERNAME_INPUT = "//input[@id='input-username']"
    PASSWORD_INPUT = "//input[@id='input-password']"
    LOGIN_BUTTON = "//button[@type='submit']"

    def __init__(self, browser):
        super().__init__(browser)
        self.go_to_admin_login_page()

    def go_to_admin_login_page(self) -> None:
        try:
            url = f"{self.browser.base_url}/administration"
            self.browser.get(url)
        except Exception as e:
            print(f"Failed to navigate to the admin login page: {e}")

    def go_to_main_admin_panel_with_token(self, token: str) -> None:
        try:
            url = f"{self.browser.base_url}/administration/index.php?route=common/dashboard&user_token={token}"
            self.browser.get(url)
        except Exception as e:
            print(f"Failed to navigate to the main admin panel with token: {e}")

    def get_page(self, menu_item: str):
        return self.get_page_object(menu_item)

    def get_page_object(self, menu_item: str):
        if menu_item == "Dashboard":
            return AdministrationDashboardPage(self.browser)
        else:
            raise ValueError(f"Page object for {menu_item} is not defined.")

    def get_admin_header_text(self) -> str:
        try:
            return self.wait_for_element(self.ADMIN_CARD_HEADER).text
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve admin header text: {e}")
            return ""

    def fill_username(self, username: str):
        try:
            input_username_field = self.wait_for_element(self.USERNAME_INPUT)
            input_username_field.clear()
            input_username_field.send_keys(username)
        except NoSuchElementException as e:
            print(f"Error when trying to fill username: {e}")
        return self

    def fill_password(self, password: str):
        try:
            input_password_field = self.wait_for_element(self.PASSWORD_INPUT)
            input_password_field.clear()
            input_password_field.send_keys(password)
        except NoSuchElementException as e:
            print(f"Error when trying to fill password: {e}")
        return self

    def click_for_login(self):
        try:
            self.wait_for_element(self.LOGIN_BUTTON).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click the login button: {e}")
        return self

    def login_to_admin_panel(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_for_login()
