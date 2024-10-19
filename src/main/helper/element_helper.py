from typing import List

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.tests.conftest import browser


class ElementHelper:

    @staticmethod
    def get_list_items_texts(parent_element: WebElement, locator: By = By.TAG_NAME, tag: str = "li") -> List[str]:
        try:
            li_elements = parent_element.find_elements(locator, tag)
            return [li.text.strip() for li in li_elements if li.text.strip()]
        except (NoSuchElementException, StaleElementReferenceException):
            return []

    @staticmethod
    def get_text_for_locator(browser, path: str, locator: By = By.XPATH):
        try:
            element = browser.find_element(locator, path)
            return element.text.strip()
        except (NoSuchElementException, StaleElementReferenceException):
            return None
