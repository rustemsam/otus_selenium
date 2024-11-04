import allure
import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge",
    )
    parser.addoption(
        "--base_url",
        default="http://192.168.1.47:8081",
        help="Base URL for the application",
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome != "passed":
        item.status = "failed"
    else:
        item.status = "passed"


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    base_url = request.config.getoption("--base_url")
    driver = None

    if browser_name in ["ch", "chrome"]:
        driver = webdriver.Chrome()
    elif browser_name in ["ff", "firefox"]:
        driver = webdriver.Firefox()
    elif browser_name in ["ed", "edge"]:
        driver = webdriver.Edge()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.base_url = base_url
    yield driver

    if request.node.status == "failed":
        allure.attach(
            name="failure_screenshot",
            body=driver.get_screenshot_as_png(),
            attachment_type=allure.attachment_type.PNG,
        )
        allure.attach(
            name="page_source",
            body=driver.page_source,
            attachment_type=allure.attachment_type.HTML,
        )
    driver.quit()
