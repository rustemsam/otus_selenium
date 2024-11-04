from typing import List

import allure
from selenium.common import NoSuchElementException

from src.main.pages.base_page import BasePage


class BottomPanel(BasePage):
    BOTTOM_PANEL = "//div/*[contains(text(),'{}')]/../ul"

    @allure.step("Getting bottom panel options for '{option}'")
    def get_bottom_panel_options(self, option: str) -> List[str]:
        try:
            ul_element = self.wait_for_element(self.BOTTOM_PANEL.format(option))
            options = self.get_items_text(ul_element)
            return options
        except NoSuchElementException:
            self.logger.warning(f"Bottom panel for option '{option}' not found.")
            return []
