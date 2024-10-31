from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from src.main.pages.base_page import BasePage
from src.main.pages.catalog.cameras.canon_page import CanonPage
from src.main.pages.catalog.catalog_page import CatalogPage
from src.main.pages.catalog.desktops.apple_mac_page import ApplePage


class HomePage(BasePage):
    MENU = "//*[contains(text(),'{}')]"
    SHOW_ALL = "//*[contains(text(),'Show All {}')]"
    CATEGORIES = "//ul[@class='nav navbar-nav']"
    FEATURED_ITEMS = "//*[contains(text(),'Featured')]/../div[2]"
    ITEM_TO_CARD = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//button[@title='Add to Cart']"
    PRODUCT_PRICE = "//h4/a[contains(text(), '{}')]//ancestor::div[contains(@class, 'product-thumb')]//span[@class='price-new']"

    PRODUCT_PAGE_MAPPING = {
        "canon": CanonPage,
        "apple": ApplePage,
    }

    def __init__(self, browser):
        super().__init__(browser)
        self.go_to_home_page()

    def go_to_home_page(self):
        self.browser.get(self.browser.base_url)

    def go_to_page(self, menu_item: str):
        try:
            self.wait_for_element(self.MENU.format(menu_item)).click()
            self.wait_for_element(self.SHOW_ALL.format(menu_item)).click()
            return self.get_page_object(menu_item)
        except NoSuchElementException as e:
            print(f"Error when was going  to page '{menu_item}': {e}")
            return None

    def get_page_object(self, menu_item: str):
        page_objects = {
            "Desktops": CatalogPage(self.browser),
        }
        try:
            return page_objects[menu_item]
        except KeyError:
            raise ValueError(f"Page object for {menu_item} is not defined.")

    def get_list_categories(self) -> list:
        try:
            categories = self.wait_for_element(self.CATEGORIES)
            return self.get_items_text(categories)
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve categories: {e}")
            return []

    def get_items_on_featured(self) -> list:
        try:
            element = self.wait_for_element(self.FEATURED_ITEMS)
            return element.find_elements(By.XPATH, "div")
        except NoSuchElementException as e:
            print(f"Error when trying to retrieve featured items: {e}")
            return []

    def get_price_of_product(self, product_name: str) -> str:
        try:
            return self.wait_for_element(self.PRODUCT_PRICE.format(product_name)).text
        except NoSuchElementException as e:
            print(
                f"Error when trying to retrieve price for product '{product_name}': {e}"
            )
            return "0.0"

    def add_item_to_basket(self, item: str) -> None:
        try:
            initial_url = self.browser.current_url
            element = self.wait_for_element_to_be_clickable(
                self.ITEM_TO_CARD.format(item)
            )
            self.js_click_to_element(element)

            WebDriverWait(self.browser, 5).until(
                lambda driver: driver.current_url != initial_url
            )
            current_url = self.browser.current_url
            if initial_url == current_url:
                return
            else:
                matching_class = next(
                    (
                        cls
                        for keyword, cls in self.PRODUCT_PAGE_MAPPING.items()
                        if keyword in current_url
                    ),
                    None,
                )
                if matching_class:
                    product_page = matching_class(self.browser)
                    product_page.select_options()
                    product_page.add_item_to("card")
                else:
                    print(f"No specific handler for URL: {current_url}")
                    return

        except NoSuchElementException as e:
            print(f"Error when trying to add item '{item}' to basket: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
