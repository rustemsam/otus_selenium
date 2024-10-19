from typing import Optional

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class WaitHelper:
    DEFAULT_TIMEOUT = 10

    @staticmethod
    def _wait_with_timeout(browser, timeout: int):
        return WebDriverWait(browser, timeout)

    @staticmethod
    def wait_for_element(
        browser, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Optional[WebElement]:
        try:
            wait = WaitHelper._wait_with_timeout(browser, timeout)
            return wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            print(
                f"Element with locator {xpath} was not found for the time {timeout} seconds"
            )
            return None

    @staticmethod
    def wait_for_element_to_be_clickable(
        browser, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ) -> Optional[WebElement]:
        try:
            wait = WaitHelper._wait_with_timeout(browser, timeout)
            return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        except TimeoutException:
            print(
                f"Element with locator '{xpath}' was not clickable within {timeout} seconds."
            )
            return None

    @staticmethod
    def wait_for_new_page_loaded(
        browser, url: str, timeout: int = DEFAULT_TIMEOUT
    ) -> bool:
        try:
            wait = WaitHelper._wait_with_timeout(browser, timeout)
            return wait.until(EC.url_contains(url))
        except TimeoutException:
            print(
                f"Page did not load with URL containing '{url}' within {timeout} seconds."
            )
            return False

    @staticmethod
    def wait_for_element_to_disappear(
        browser, xpath: str, timeout: int = DEFAULT_TIMEOUT
    ):
        try:
            wait = WaitHelper._wait_with_timeout(browser, timeout)
            alert_present = wait.until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            return wait.until(EC.invisibility_of_element(alert_present))
        except TimeoutException:
            print(
                f"Element with locator '{xpath}' didn't disappear within {timeout} seconds."
            )
