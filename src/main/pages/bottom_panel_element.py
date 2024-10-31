from selenium.common import NoSuchElementException

from src.main.pages.base_page import BasePage


class BottomPanel(BasePage):
    BOTTOM_PANEL = "//div/*[contains(text(),'{}')]/../ul"

    def get_bottom_panel_options(self, option: str) -> list:
        try:
            ul_element = self.wait_for_element(self.BOTTOM_PANEL.format(option))
            return self.get_items_text(ul_element)
        except NoSuchElementException:
            print(f"Bottom panel for option '{option}' not found.")
            return []
