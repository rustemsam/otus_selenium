import pytest

from src.main.helper.config_helper import ConfigHelper
from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper

ADMIN_CARD_HEADER = "//div[@class='card-header']"
USERNAME_INPUT = "//input[@id='input-username']"
PASSWORD_INPUT = "//input[@id='input-password']"
LOGIN_BUTTON = "//button[@type='submit']"
ALERT_FAILURE = "//div[@class='alert alert-danger alert-dismissible']"
PAGE_HEADER = "//div[@class='page-header']/div/h1"


@pytest.fixture(scope="session")
def wait_helper():
    return WaitHelper()


@pytest.fixture(scope="session")
def element_helper():
    return ElementHelper()


@pytest.fixture(autouse=True)
def run_around_tests(browser):
    url = f"{browser.base_url}/administration"
    browser.get(url)


def test_admin_header(browser, wait_helper):
    header_text = get_admin_header_text(browser, wait_helper)
    expected_text = "Please enter your login details."
    assert (
        expected_text == header_text
    ), f"Expected text is {expected_text}, but got {header_text}"


def test_admin_login(browser, wait_helper):
    login_to_admin_panel(
        browser,
        wait_helper,
        ConfigHelper.get_key("ADMIN_LOGIN"),
        ConfigHelper.get_key("ADMIN_PASSWORD"),
    )

    page_header = get_admin_dashboard_page_header(browser, wait_helper)
    expected_text = "Dashboard"
    assert (
        expected_text == page_header
    ), f"Expected text is {expected_text}, but got {page_header}"


def test_admin_login_without_password(browser, wait_helper):
    fill_username(browser, wait_helper, "admin")
    click_for_login(browser, wait_helper)

    text = get_failure_alert_text(browser, wait_helper)
    expected_text = "No match for Username and/or Password."
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


def test_admin_login_with_wrong_password(browser, wait_helper):
    login_to_admin_panel(browser, wait_helper, "admin", "_+!")

    text = get_failure_alert_text(browser, wait_helper)
    expected_text = "No match for Username and/or Password."
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


def test_admin_login_with_wrong_session(browser, wait_helper):
    invalid_token = "04ae8e91e7e24c295ccf4d7bcab3bd851"
    go_to_main_admin_panel_with_token(browser, invalid_token)
    text = get_failure_alert_text(browser, wait_helper)
    expected_text = "Invalid token session. Please login again."
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


def get_admin_header_text(browser, wait_helper) -> str:
    return wait_helper.wait_for_element(browser, ADMIN_CARD_HEADER).text


def login_to_admin_panel(browser, wait_helper, username: str, password: str):
    fill_username(browser, wait_helper, username)
    fill_password(browser, wait_helper, password)
    click_for_login(browser, wait_helper)


def fill_username(browser, wait_helper, username: str) -> None:
    input_username_field = wait_helper.wait_for_element(browser, USERNAME_INPUT)
    input_username_field.clear()
    input_username_field.send_keys(username)


def fill_password(browser, wait_helper, password: str) -> None:
    input_password_field = wait_helper.wait_for_element(browser, PASSWORD_INPUT)
    input_password_field.clear()
    input_password_field.send_keys(password)


def click_for_login(browser, wait_helper) -> None:
    wait_helper.wait_for_element(browser, LOGIN_BUTTON).click()


def get_admin_dashboard_page_header(browser, wait_helper) -> str:
    header_element = wait_helper.wait_for_element(browser, PAGE_HEADER)
    return header_element.text


def get_failure_alert_text(browser, wait_helper) -> str:
    return wait_helper.wait_for_element(browser, ALERT_FAILURE).text


def go_to_main_admin_panel_with_token(browser, token: str) -> None:
    url = f"{browser.base_url}/administration/index.php?route=common/dashboard&user_token={token}"
    browser.get(url)
