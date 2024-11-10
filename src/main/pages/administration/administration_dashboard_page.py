from selenium.common import NoSuchElementException

from src.main.pages.base_page import BasePage


class AdministrationDashboardPage(BasePage):
    PAGE_HEADER = "//div[@class='page-header']/div/h1"

    def get_admin_dashboard_page_header(self) -> str:
        try:
            header_element = self.wait_for_element(self.PAGE_HEADER)
            return header_element.text
        except NoSuchElementException as e:
            print(f"Page header element not found: {e}")
