import pytest
from selenium import webdriver

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge"
    )
    parser.addoption(
        "--base_url",
        default="http://192.168.1.47:8081",
        help="Base URL for the application"
    )

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
    driver.quit()
