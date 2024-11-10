from selenium.common import NoSuchElementException

from src.main.pages.base_page import BasePage


class AlertElement(BasePage):
    SUCCESS_ALERT = "//div[@class='alert alert-success alert-dismissible']"
    FAILURE_ALERT = "//*[@class='alert alert-danger alert-dismissible']"
    ALERT_DANGER = "//div[contains(@class,'alert-danger')]"

    def wait_until_successful_alert_disappeared(self) -> None:
        try:
            self.wait_for_element_to_disappear(self.SUCCESS_ALERT)
        except NoSuchElementException:
            print("Success alert not found")

    def get_successfully_text_alert(self) -> str:
        return self.wait_for_element_to_be_clickable(self.SUCCESS_ALERT).text

    def get_failure_text_alert(self) -> str:
        try:
            alert_element = self.wait_for_element(self.FAILURE_ALERT, timeout=10)
            return alert_element.text
        except NoSuchElementException:
            self.logger.info("Failure alert did not appear within the timeout period.")
