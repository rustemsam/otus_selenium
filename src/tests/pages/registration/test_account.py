import time

import pytest
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from src.main.helper.element_helper import ElementHelper
from src.main.helper.wait_helper import WaitHelper
from src.main.models.login_model import AccountRequestBody

INPUT_FIRST_NAME = "//input[@id='input-firstname']"
INPUT_LAST_NAME = "//input[@id='input-lastname']"
INPUT_EMAIL = "//input[@id='input-email']"
INPUT_PASSWORD = "//input[@id='input-password']"
FIRST_NAME_VALIDATION = "//div[@id='error-firstname']"
LAST_NAME_VALIDATION = "//div[@id='error-lastname']"
EMAIL_VALIDATION = "//div[@id='error-email']"
PASSWORD_VALIDATION = "//div[@id='error-password']"
BOTTOM_XPATH = "window.scrollTo(0, document.body.scrollHeight);"
AGREE_CHECKBOX = "//input[@name='agree']"
SUBMIT_BUTTON = "//button[@type='submit']"
JS_ARGUMENT_CLICK = "arguments[0].click();"
EMAIL = "email"
JS_VALIDATION_MESSAGE = "return arguments[0].validationMessage;"
FAILURE_ALERT = "//dirv[@class='alert alert-danger alert-dismissible']"
SUCCESSFUL_REGISTRATION = "//div[@id='common-success']/div/div/h1"
INPUT_EMAIL_NAME = "//input[@id='input-email']"
INPUT_PASSWORD_NAME = "//input[@id='input-password']"
ALERT_DANGER = "//div[contains(@class,'alert-danger')]"
ACCOUNT_CONTENT = "//div[@id='content']"


@pytest.fixture(scope="session")
def wait_helper():
    return WaitHelper()


@pytest.fixture(scope="session")
def element_helper():
    return ElementHelper()


@pytest.fixture(autouse=True)
def run_around_tests(browser):
    url = f"{browser.base_url}/index.php?route=account/register"
    browser.get(url)


@pytest.fixture
def create_user_fixture(browser, wait_helper):
    post_request = AccountRequestBody(
        first_name="first",
        last_name="last",
        email="teczxst@test.com",
        password="qwerty123",
    )
    create_user(browser, wait_helper, post_request)
    return post_request


def test_account_registration(browser, wait_helper):
    ts = int(time.time())
    post_request = AccountRequestBody(
        first_name=f"test+{ts}",
        last_name=f"last_name+{ts}",
        email=f"test_{ts}@test.com",
        password="qwerty123",
    )
    create_user(browser, wait_helper, post_request)

    successful_registration_text = get_successful_registration_message(
        browser, wait_helper
    )
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
def test_account_registration_with_invalid_data(browser, wait_helper, post_request):
    create_user(browser, wait_helper, post_request)

    text_first_name = get_validation_error(browser, wait_helper, "first_name")
    text_last_name = get_validation_error(browser, wait_helper, "last_name")
    text_email = get_validation_error(browser, wait_helper, "email")
    text_password = get_validation_error(browser, wait_helper, "password")

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
def test_account_registration_with_invalid_email(
    browser, wait_helper, email, expected_test
):
    post_request = AccountRequestBody(
        first_name="first_name",
        last_name="last_name",
        email=email,
        password="qwerty123",
    )

    create_user(browser, wait_helper, post_request)
    validation_message = get_pop_up_email_validation_error(browser)
    assert (
        expected_test == validation_message
    ), f"Expected text is {expected_test}, but got {validation_message}"


def test_account_registration_without_policy_agree(browser, wait_helper):
    ts = int(time.time())
    post_request = AccountRequestBody(
        first_name=f"test+{ts}",
        last_name=f"last_name+{ts}",
        email=f"test_{ts}@test.com",
        password="qwerty123",
    )

    create_user(browser, wait_helper, post_request, agree_checkbox=False)

    text = get_text_from_failure_alert(browser, wait_helper)
    expected_text = "Warning: You must agree to the Privacy Policy!"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


def test_account_registration_with_same_email(
    browser, wait_helper, create_user_fixture
):
    post_request = create_user_fixture
    url = f"{browser.base_url}/index.php?route=account/register"
    browser.get(url)
    create_user(browser, wait_helper, post_request)
    text = get_text_from_failure_alert(browser, wait_helper)
    expected_text = "Warning: E-Mail Address is already registered!"
    assert expected_text == text, f"Expected text is {expected_text}, but got {text}"


# 3.1. автотест логина-разлогина в админку с проверкой, что логин был выполнен
def test_account_login(browser, wait_helper, element_helper, create_user_fixture):
    post_request = create_user_fixture
    url = f"{browser.base_url}//index.php?route=account/login"
    browser.get(url)
    login_to_account(browser, wait_helper, post_request.email, post_request.password)

    if personal_account_is_opened(browser, wait_helper):
        print("Login successful.")
    else:
        print("Login unsuccessful, checking for alerts.")

        try:
            alert_message = get_text_from_alert_danger(browser, wait_helper)

            if "Invalid token session" in alert_message:
                print("Session token expired during login attempt.")
                browser.refresh()
                login_to_account(
                    browser, wait_helper, post_request.email, post_request.password
                )
                wait_for_account_page_loaded(browser, wait_helper)
            else:
                print(f"Login failed with alert message: {alert_message}")

        except NoSuchElementException:
            print("Login attempt failed, but no alert was found.")
            raise Exception("Login failed without an error message.")

    account_sections = get_account_sections(browser, wait_helper, element_helper)
    expected_list = ["My Account", "My Orders", "My Affiliate Account", "Newsletter"]

    assert (
        expected_list == account_sections
    ), f"Expected list is {expected_list}, but got {account_sections}"


def create_user(
    browser,
    wait_helper,
    account_request_body: AccountRequestBody,
    agree_checkbox: bool = "true",
) -> AccountRequestBody:
    fill_input_field(
        browser, wait_helper, INPUT_FIRST_NAME, account_request_body.first_name
    )
    fill_input_field(
        browser, wait_helper, INPUT_LAST_NAME, account_request_body.last_name
    )
    fill_input_field(browser, wait_helper, INPUT_EMAIL, account_request_body.email)
    fill_input_field(
        browser, wait_helper, INPUT_PASSWORD, account_request_body.password
    )

    if agree_checkbox:
        agree_checkbox = wait_helper.wait_for_element(browser, AGREE_CHECKBOX)
        browser.execute_script(JS_ARGUMENT_CLICK, agree_checkbox)

    submit_button = wait_helper.wait_for_element_to_be_clickable(browser, SUBMIT_BUTTON)
    browser.execute_script(JS_ARGUMENT_CLICK, submit_button)

    return account_request_body


def fill_input_field(browser, wait_helper, locator: str, value: str) -> None:
    element = wait_helper.wait_for_element(browser, locator)
    element.clear()
    element.send_keys(value)


def get_validation_error(browser, wait_helper, field_name: str) -> str:
    validation_xpath = {
        "first_name": FIRST_NAME_VALIDATION,
        "last_name": LAST_NAME_VALIDATION,
        "email": EMAIL_VALIDATION,
        "password": PASSWORD_VALIDATION,
    }.get(field_name)

    return (
        wait_helper.wait_for_element(browser, validation_xpath).text
        if validation_xpath
        else ""
    )


def get_successful_registration_message(browser, wait_helper) -> str:
    return wait_helper.wait_for_element(browser, SUCCESSFUL_REGISTRATION).text


def get_pop_up_email_validation_error(browser) -> str:
    email_field = browser.find_element(By.NAME, EMAIL)
    return browser.execute_script(JS_VALIDATION_MESSAGE, email_field)


def get_text_from_failure_alert(browser, wait_helper) -> str:
    return wait_helper.wait_for_element(browser, FAILURE_ALERT).text


def login_to_account(browser, wait_helper, login: str, password: str) -> None:
    try:
        fill_input_field(browser, wait_helper, INPUT_EMAIL_NAME, login)
        fill_input_field(browser, wait_helper, INPUT_PASSWORD_NAME, password)

        wait_helper.wait_for_element_to_be_clickable(browser, SUBMIT_BUTTON).click()
    except Exception as e:
        print(f"Error during retry login: {str(e)}")


def personal_account_is_opened(browser, wait_helper) -> bool:
    try:
        wait_for_account_page_loaded(browser, wait_helper, 2)
        is_opened = True
    except TimeoutException:
        print("Page did not load correctly after login within the expected time.")
        is_opened = False
    return is_opened


def get_account_sections(browser, wait_helper, element_helper) -> list:
    content = wait_helper.wait_for_element(browser, ACCOUNT_CONTENT)
    return element_helper.get_list_items_texts(content, tag="h2")


def wait_for_account_page_loaded(browser, wait_helper, timeout: int = 10):
    wait_helper.wait_for_new_page_loaded(browser, "account&customer_token=", timeout)


def get_text_from_alert_danger(browser, wait_helper) -> str:
    return wait_helper.wait_for_element(browser, ALERT_DANGER).text
