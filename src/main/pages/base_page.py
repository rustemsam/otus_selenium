from typing import List, Optional

from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    DEFAULT_TIMEOUT = 10
    JS_ARGUMENT_CLICK = "arguments[0].click();"
    JS_ARGUMENT_SCROLL = "arguments[0].scrollIntoView(true);"

    def __init__(self, browser):
        self.browser = browser

    def input_value(self, locator: str, value: str) -> None:
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(value)

    def get_items_text(
        self, parent_element: WebElement, locator: By = By.TAG_NAME, tag: str = "li"
    ) -> List[str]:
        try:
            li_elements = parent_element.find_elements(locator, tag)
            return [li.text.strip() for li in li_elements if li.text.strip()]
        except (NoSuchElementException, StaleElementReferenceException):
            return []

    def get_text(self, path: str, locator: By = By.XPATH):
        try:
            element = self.browser.find_element(locator, path)
            return element.text.strip()
        except (NoSuchElementException, StaleElementReferenceException):
            return None

    def _wait_with_timeout(self, timeout: int):
        return WebDriverWait(self.browser, timeout)

    def wait_for_element(
        self, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Optional[WebElement]:
        try:
            wait = self._wait_with_timeout(timeout)
            return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print(
                f"Element with locator {xpath} was not found for the time {timeout} seconds"
            )
            return None

    def wait_for_element_to_be_clickable(
        self, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Optional[WebElement]:
        try:
            wait = self._wait_with_timeout(timeout)
            return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            print(
                f"Element with locator '{xpath}' was not clickable within {timeout} seconds."
            )
            return None

    def wait_for_new_page_loaded(
        self, url: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        try:
            wait = self._wait_with_timeout(timeout)
            return wait.until(EC.url_contains(url))
        except TimeoutException:
            print(
                f"Page did not load with URL containing '{url}' within {timeout} seconds."
            )
            return False

    def wait_for_element_to_disappear(self, xpath: str, timeout: int = DEFAULT_TIMEOUT):
        try:
            wait = self._wait_with_timeout(timeout)
            alert_present = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return wait.until(EC.invisibility_of_element(alert_present))
        except TimeoutException:
            print(
                f"Element with locator '{xpath}' didn't disappear within {timeout} seconds."
            )

    def scroll_to_element(self, element):
        self.browser.execute_script(self.JS_ARGUMENT_SCROLL, element)

    def js_click_to_element(self, element):
        self.browser.execute_script(self.JS_ARGUMENT_CLICK, element)

    def maximize_browser_window(self):
        self.browser.maximize_window()

    def click_using_action(self, locator):
        actions = ActionChains(self.browser)
        actions.move_to_element(self.wait_for_element(locator)).click().perform()
