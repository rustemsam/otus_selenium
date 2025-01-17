import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to run tests: chrome, firefox, edge",
    )
    parser.addoption(
        "--base_url",
        default="http://192.168.1.196:8081",
        help="Base URL for the application",
    )
    parser.addoption(
        "--remote",
        action="store_true",
        help="Run tests on Selenoid (remote execution)",
    )
    parser.addoption(
        "--selenium_url",
        default="http://localhost:4444/wd/hub",
        help="URL to the Selenoid executor",
    )
    parser.addoption(
        "--vnc",
        action="store_true",
        help="Enable VNC support for Selenoid (view live browser sessions)",
    )
    parser.addoption(
        "--logs",
        action="store_true",
        help="Enable browser log collection for Selenoid sessions",
    )
    parser.addoption(
        "--video",
        action="store_true",
        help="Enable video recording for Selenoid sessions",
    )
    parser.addoption(
        "--bv",
        default=None,
        help="Browser version to use in tests",
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
    remote = request.config.getoption("--remote")
    selenium_url = request.config.getoption("--selenium_url")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")

    driver = None
    options = None

    if remote:
        if browser_name == "chrome":
            options = ChromeOptions()
        elif browser_name == "firefox":
            options = FirefoxOptions()
        elif browser_name == "edge":
            options = EdgeOptions()
        else:
            raise ValueError(f"Unsupported browser for remote execution: {browser_name}")

        caps = {
            "browserName": browser_name,
            "browserVersion": version,
            "selenoid:options": {
                "enableVNC": vnc,
                "name": request.node.name,
                "screenResolution": "1280x2000",
                "enableVideo": video,
                "enableLog": logs,
                "timeZone": "Europe/Moscow",
                "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]
            },
            "acceptInsecureCerts": True,
        }

        capabilities = options.to_capabilities()
        capabilities.update(caps)
        for k, v in caps.items():
            options.set_capability(k, v)
        driver = RemoteWebDriver(
            command_executor=selenium_url,
            options=options
        )
    else:
        if browser_name == "chrome":
            options = ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            driver = webdriver.Chrome(options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)

        elif browser_name == "edge":
            options = EdgeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
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
