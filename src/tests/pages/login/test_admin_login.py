from src.main.helper.config_helper import ConfigHelper
from src.main.pages.administration.administration_login_page import AdministrationLoginPage


def test_admin_header(browser):
    admin_page = AdministrationLoginPage(browser)
    header_text = admin_page.get_admin_header_text()
    expected_text = "Please enter your login details."
    assert (
            expected_text == header_text
    ), f"Expected text is {expected_text}, but got {header_text}"


def test_admin_login(browser):
    admin_page = AdministrationLoginPage(browser)
    admin_page.login_to_admin_panel(ConfigHelper.get_key("ADMIN_LOGIN"), ConfigHelper.get_key("ADMIN_PASSWORD"))
    admin_dashboard_page = admin_page.get_page("Dashboard")
    page_header = admin_dashboard_page.get_admin_dashboard_page_header()
    expected_text = "Dashboard"
    assert (
            expected_text == page_header
    ), f"Expected text is {expected_text}, but got {page_header}"


def test_admin_login_without_password(browser):
    admin_page = AdministrationLoginPage(browser)
    admin_page.fill_username("admin")
    admin_page.click_for_login()

    text = admin_page.get_failure_alert_text()
    expected_text = "No match for Username and/or Password."
    assert (
            expected_text == text
    ), f"Expected text is {expected_text}, but got {text}"


def test_admin_login_with_wrong_password(browser):
    admin_page = AdministrationLoginPage(browser)
    admin_page.login_to_admin_panel("admin", "_+!")

    text = admin_page.get_failure_alert_text()
    expected_text = "No match for Username and/or Password."
    assert (
            expected_text == text
    ), f"Expected text is {expected_text}, but got {text}"


def test_admin_login_with_wrong_session(browser):
    admin_page = AdministrationLoginPage(browser)
    invalid_token = "04ae8e91e7e24c295ccf4d7bcab3bd851"
    admin_page.go_to_main_admin_panel_with_token(invalid_token)
    text = admin_page.get_failure_alert_text()
    expected_text = "Invalid token session. Please login again."
    assert (
            expected_text == text
    ), f"Expected text is {expected_text}, but got {text}"
