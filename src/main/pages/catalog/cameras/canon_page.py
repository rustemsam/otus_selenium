from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from src.main.pages.catalog.catalog_page import CatalogPage


class CanonPage(CatalogPage):
    COLOUR_OPTION = "//select[@name='option[226]']"
    COLOUR_OPTION_VALUE = (
        "//select[@id='input-option-226']/option[contains(text(),'{}')]"
    )

    def __init__(self, browser):
        super().__init__(browser)
        self.maximize_browser_window()

    def select_options(self, colour="Blue"):
        try:
            colour_dropdown = self.wait_for_element(self.COLOUR_OPTION)
            self.scroll_to_element(colour_dropdown)
            select = Select(colour_dropdown)
            select.select_by_visible_text(colour)

            colour_option = self.wait_for_element(
                self.COLOUR_OPTION_VALUE.format(colour)
            )
            colour_option.click()
        except NoSuchElementException as e:
            print(f"Error when trying to select color '{colour}': {e}")