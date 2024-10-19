from selenium.common import NoSuchElementException

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper


class AdministrationDashboardPage:
    PAGE_HEADER = "//div[@class='page-header']/div/h1"

    def __init__(self, browser):
        self.browser = browser
        self.wait_helper = WaitHelper()
        self.element_helper = ElementHelper()

    def get_admin_dashboard_page_header(self) -> str:
        try:
            header_element = self.wait_helper.wait_for_element(
                self.browser, self.PAGE_HEADER
            )
            return header_element.text
        except NoSuchElementException as e:
            print(f"Page header element not found: {e}")
            return "Header not found"
