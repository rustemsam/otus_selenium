import allure

from src.main.helper.config_helper import ConfigHelper
from src.main.pages.administration.administration_dashboard_page import (
    AdministrationDashboardPage,
)
from src.main.pages.administration.administration_login_page import (
    AdministrationLoginPage,
)
from src.main.pages.alert_element import AlertElement


@allure.title("Check the header text of the admin page")
def test_admin_header(browser):
    admin_page = AdministrationLoginPage(browser)
    header_text = admin_page.get_admin_header_text()
    expected_text = "Please enter your login details."
    assert (
        expected_text == header_text
    ), f"Expected text is {expected_text}, but got {header_text}"


@allure.title("Check the login to the admin panel")
def test_admin_login(browser):
    admin_page = AdministrationLoginPage(browser)
    admin_page.login_to_admin_panel(
        ConfigHelper.get_key("ADMIN_LOGIN"), ConfigHelper.get_key("ADMIN_PASSWORD")
    )
    admin_dashboard = AdministrationDashboardPage(browser)
    page_header = admin_dashboard.get_admin_dashboard_page_header()
    expected_text = "Dashboard"
    assert (
        expected_text == page_header
    ), f"Expected text is {expected_text}, but got {page_header}"


@allure.title("Check the validation message when trying to login without password")
def test_admin_login_without_password(browser):
    admin_page = AdministrationLoginPage(browser)

    (admin_page.fill_username("admin").click_for_login())

    alert = AlertElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "No match for Username and/or Password."
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


@allure.title("Check the validation when trying to login with wrong password")
def test_admin_login_with_wrong_password(browser):
    admin_page = AdministrationLoginPage(browser)
    admin_page.login_to_admin_panel("admin", "_+!")

    alert = AlertElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "No match for Username and/or Password."
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


@allure.title("Check the validation when trying to login with wrong session")
def test_admin_login_with_wrong_session(browser):
    invalid_token = "04ae8e91e7e24c295ccf4d7bcab3bd851"
    admin_page = AdministrationLoginPage(browser)
    admin_page.go_to_main_admin_panel_with_token(invalid_token)
    alert = AlertElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "Invalid token session. Please login again."
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"
