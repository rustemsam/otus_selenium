import time

import allure
import pytest
from selenium.common import NoSuchElementException

from src.main.models.login_model import AccountRequestBody
from src.main.pages.alert_element import AlertElement
from src.main.pages.my_account.account_login_page import AccountLoginPage
from src.main.pages.my_account.account_register_page import AccountRegisterPage


@pytest.fixture
def create_user_fixture(browser):
    post_request = AccountRequestBody(
        first_name="first",
        last_name="last",
        email="l7.test@test.com",
        password="qwerty123",
    )
    account_page = AccountRegisterPage(browser)
    account_page.create_user(post_request)
    return post_request


@allure.title("Check the registration of test account")
def test_account_registration(browser):
    ts = int(time.time())
    post_request = AccountRequestBody(
        first_name=f"test+{ts}",
        last_name=f"last_name+{ts}",
        email=f"test_{ts}@test.com",
        password="qwerty123",
    )
    account_page = AccountRegisterPage(browser)
    account_page.create_user(post_request)

    successful_registration_text = account_page.get_successful_registration_message()
    expected_text = "Your Account Has Been Created!"
    assert (
        expected_text == successful_registration_text
    ), f"Expected text is {expected_text}, but got {successful_registration_text}"


@pytest.mark.parametrize(
    "post_request",
    [
        AccountRequestBody(
            first_name="",
            last_name="f4wcYnrgUe2bHSrJWLpURHpOaTSZvagD1",
            email="",
            password="123",
        ),
        AccountRequestBody(
            first_name="f4wcYnrgUe2bHSrJWLpURHpOaTSZvagD!",
            last_name="",
            email="",
            password="nQOH1NvCpj6TJS5zIfGJD",
        ),  # TODO: BUG 5
    ],
)
@allure.title("Check the registration of test account with invalid data")
def test_account_registration_with_invalid_data(browser, post_request):
    account_page = AccountRegisterPage(browser)
    account_page.create_user(post_request)

    text_first_name = account_page.get_validation_error("first_name")
    text_last_name = account_page.get_validation_error("last_name")
    text_email = account_page.get_validation_error("email")
    text_password = account_page.get_validation_error("password")

    expected_first_name_text = "First Name must be between 1 and 32 characters!"
    expected_last_name_text = "Last Name must be between 1 and 32 characters!"
    expected_password_text = "Password must be between 4 and 20 characters!"
    expected_email_text = "E-Mail Address does not appear to be valid!"

    assert (
        expected_first_name_text == text_first_name
    ), f"Expected text is {text_first_name}, but got {text_first_name}"
    assert (
        expected_last_name_text == text_last_name
    ), f"Expected text is {expected_last_name_text}, but got {text_last_name}"
    assert (
        expected_password_text == text_password
    ), f"Expected text is {expected_password_text}, but got {text_password}"
    assert (
        expected_email_text == text_email
    ), f"Expected text is {expected_email_text}, but got {text_email}"


@pytest.mark.parametrize(
    "email, expected_test",
    [
        ("_@_.com", "A part following '@' should not contain the symbol '_'."),
        ("1@.com", "'.' is used at a wrong position in '.com'."),
        (
            "test.com",
            "Please include an '@' in the email address. 'test.com' is missing an '@'.",
        ),
        ("@.com", "Please enter a part followed by '@'. '@.com' is incomplete."),
    ],
)
@allure.title("Check the registration of test account with invalid email")
def test_account_registration_with_invalid_email(browser, email, expected_test):
    post_request = AccountRequestBody(
        first_name="first_name",
        last_name="last_name",
        email=email,
        password="qwerty123",
    )
    account_page = AccountRegisterPage(browser)
    account_page.create_user(post_request)
    validation_message = account_page.get_pop_up_email_validation_error()
    assert (
        expected_test == validation_message
    ), f"Expected text is {expected_test}, but got {validation_message}"


@allure.title("Check the registration of test account without policy agreeing")
def test_account_registration_without_policy_agree(browser):
    ts = int(time.time())
    post_request = AccountRequestBody(
        first_name=f"test+{ts}",
        last_name=f"last_name+{ts}",
        email=f"test_{ts}@test.com",
        password="qwerty123",
    )
    account_page = AccountRegisterPage(browser)
    account_page.create_user(post_request, agree_checkbox=False)
    alert = AlertElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "Warning: You must agree to the Privacy Policy!"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


@allure.title("Check the registration of test account with email already registered")
def test_account_registration_with_same_email(browser, create_user_fixture):
    post_request = create_user_fixture
    account_page = AccountRegisterPage(browser)
    account_page.create_user(post_request)
    alert = AlertElement(browser)
    text = alert.get_failure_text_alert()
    expected_text = "Warning: E-Mail Address is already registered!"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


# 3.1. автотест логина-разлогина в админку с проверкой, что логин был выполнен
@allure.title("Check the login to the account")
def test_account_login(browser, create_user_fixture):
    post_request = create_user_fixture
    account_login = AccountLoginPage(browser)
    account_login.login_to_account(post_request.email, post_request.password)
    alert = AlertElement(browser)

    if account_login.personal_account_is_opened():
        print("Login successful.")
    else:
        print("Login unsuccessful, checking for alerts.")
        try:
            alert_message = alert.get_failure_text_alert()
            print(f"Alert message on login failure: '{alert_message}'")
            if "Invalid token session" in alert_message:
                print("Session token expired during login attempt.")
                browser.refresh()
                account_login.login_to_account(
                    post_request.email, post_request.password
                )
                account_login.wait_for_account_page_loaded()
            else:
                print(f"Login failed with alert message: {alert_message}")
        except NoSuchElementException:
            print("Login attempt failed, but no alert was found.")
            raise Exception("Login failed without an error message.")

    account_sections = account_login.get_account_sections()
    expected_list = ["My Account", "My Orders", "My Affiliate Account", "Newsletter"]

    assert (
        expected_list == account_sections
    ), f"Expected list is {expected_list}, but got {account_sections}"
