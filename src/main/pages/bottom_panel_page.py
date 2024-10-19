from selenium.common import NoSuchElementException

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper


class BottomPanelPage:
    BOTTOM_PANEL = "//div/*[contains(text(),'{}')]/../ul"

    def __init__(self, browser):
        self.browser = browser
        self.wait_helper = WaitHelper()
        self.element_helper = ElementHelper()

    def get_bottom_panel_options(self, option: str) -> list:
        try:
            ul_element = self.wait_helper.wait_for_element(self.browser, self.BOTTOM_PANEL.format(option))
            return self.element_helper.get_list_items_texts(ul_element)
        except NoSuchElementException:
            print(f"Bottom panel for option '{option}' not found.")
            return []
