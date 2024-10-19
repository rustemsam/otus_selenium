from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from src.main.pages.base_page import BasePage
from src.main.pages.bottom_panel_page import BottomPanelPage
from src.main.pages.catalog.catalog_page import CatalogPage
from src.main.pages.top_panel_page import TopPanelPage


class HomePage(BasePage):
    MENU = "//*[contains(text(),'{}')]"
    SHOW_ALL = "//*[contains(text(),'Show All {}')]"
    CATEGORIES = "//ul[@class='nav navbar-nav']"
    FEATURED_ITEMS = "//*[contains(text(),'Featured')]/../div[2]"
    ITEM_TO_CARD = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//button[@title='Add to Cart']"
    JS_ARGUMENT_CLICK = "arguments[0].click();"
    BASKET = "//div[@class='dropdown d-grid']"
    ITEMS_IN_BASKET = "//table[@class='table table-striped mb-2']/tbody"
    PRODUCT_PRICE = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//span[@class='price-new']"

    def __init__(self, browser):
        super().__init__(browser)
        self.go_to_home_page()

    def go_to_home_page(self):
        self.browser.get(self.browser.base_url)

    def go_to_page(self, menu_item: str):
        try:
            self.wait_helper.wait_for_element(
                self.browser, self.MENU.format(menu_item)
            ).click()
            self.wait_helper.wait_for_element(
                self.browser, self.SHOW_ALL.format(menu_item)
            ).click()
            return self.get_page_object(menu_item)
        except NoSuchElementException as e:
            print(f"Error when was going  to page '{menu_item}': {e}")
            return None

    def get_panel(self, menu_item: str):
        return self.get_panel_page_object(menu_item)

    def get_page_object(self, menu_item: str):
        page_objects = {
            "Desktops": CatalogPage(self.browser),
        }
        try:
            return page_objects[menu_item]
        except KeyError:
            raise ValueError(f"Page object for {menu_item} is not defined.")

    # TODO: maybe move top/bottom to base page?
    def get_panel_page_object(self, top_bottom: str):
        panel_objects = {
            "top": TopPanelPage(self.browser),
            "bottom": BottomPanelPage(self.browser),
        }
        try:
            return panel_objects[top_bottom]
        except KeyError:
            raise ValueError(f"Page object for {top_bottom} is not defined.")

    def get_list_categories(self) -> list:
        try:
            categories = self.wait_helper.wait_for_element(
                self.browser, self.CATEGORIES
            )
            return self.element_helper.get_list_items_texts(categories)
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve categories: {e}")
            return []

    def get_items_on_featured(self) -> list:
        try:
            element = self.wait_helper.wait_for_element(
                self.browser, self.FEATURED_ITEMS
            )
            return element.find_elements(By.XPATH, "div")
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve featured items: {e}")
            return []

    def add_item_to_basket(self, item: str) -> None:
        try:
            element = self.wait_helper.wait_for_element(
                self.browser, self.ITEM_TO_CARD.format(item)
            )
            self.browser.execute_script(self.JS_ARGUMENT_CLICK, element)
            self.wait_until_successful_alert_disappeared()
        except NoSuchElementException as e:
            print(f"Error when trying to add item '{item}' to basket: {e}")

    def get_item_from_basket(self) -> list:
        try:
            self.wait_helper.wait_for_element(self.browser, self.BASKET).click()
            elements = self.wait_helper.wait_for_element(
                self.browser, self.ITEMS_IN_BASKET
            )
            return self.element_helper.get_list_items_texts(elements, tag="td")
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve items from basket: {e}")
            return []

    def get_price_of_product(self, product_name: str) -> str:
        try:
            return self.wait_helper.wait_for_element(
                self.browser, self.PRODUCT_PRICE.format(product_name)
            ).text
        except NoSuchElementException as e:
            print(
                f"Error when trying to retrieve price for product '{product_name}': {e}"
            )
            return "0.0"
