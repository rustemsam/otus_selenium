from selenium.common import NoSuchElementException

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper
from src.main.pages.administration.administration_dashboard_page import AdministrationDashboardPage


class AdministrationLoginPage:
    ADMIN_CARD_HEADER = "//div[@class='card-header']"
    USERNAME_INPUT = "//input[@id='input-username']"
    PASSWORD_INPUT = "//input[@id='input-password']"
    LOGIN_BUTTON = "//button[@type='submit']"
    ALERT_FAILURE = "//div[@class='alert alert-danger alert-dismissible']"

    def __init__(self, browser):
        self.browser = browser
        self.wait_helper = WaitHelper()
        self.element_helper = ElementHelper()
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
            return self.wait_helper.wait_for_element(self.browser, self.ADMIN_CARD_HEADER).text
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve admin header text: {e}")
            return ""

    def fill_username(self, username: str) -> None:
        try:
            input_username_field = self.wait_helper.wait_for_element(self.browser, self.USERNAME_INPUT)
            input_username_field.clear()
            input_username_field.send_keys(username)
        except NoSuchElementException as e:
            print(f"Error when trying to fill username: {e}")

    def fill_password(self, password: str) -> None:
        try:
            input_password_field = self.wait_helper.wait_for_element(self.browser, self.PASSWORD_INPUT)
            input_password_field.clear()
            input_password_field.send_keys(password)
        except NoSuchElementException as e:
            print(f"Error when trying to fill password: {e}")

    def click_for_login(self) -> None:
        try:
            self.wait_helper.wait_for_element(self.browser, self.LOGIN_BUTTON).click()
        except NoSuchElementException as e:
            print(f"Error when trying to click the login button: {e}")

    def get_failure_alert_text(self) -> str:
        try:
            return self.wait_helper.wait_for_element(self.browser, self.ALERT_FAILURE).text
        except NoSuchElementException as e:
            print(f"No failure alert found: {e}")
            return ""

    def login_to_admin_panel(self, username: str, password: str):
        self.fill_username(username)
        self.fill_password(password)
        self.click_for_login()
