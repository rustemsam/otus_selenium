## Selenium Tests

This section explains how to execute Selenium-based tests for the application. Tests can be run either locally or using Selenoid, a tool for managing Selenium WebDriver instances in Docker containers.

### Prerequisites
- Python installed with `pytest` and `selenium` packages.
- Application accessible at a specified base URL.
- [Selenoid](https://aerokube.com/selenoid/latest/) set up and running for remote execution.

### Running Tests

#### Running Tests Locally
To execute tests on your local machine, use the following command:
```bash
pytest src/tests/pages/desktops/test_desktops.py --base_url http://localhost:8081
```

#### Running Tests with Selenoid
To execute tests on your local machine, use the following command:
```bash
pytest src/tests/pages/desktops/test_desktops.py --base_url http://localhost:8081 --remote --selenium_url http://localhost:4444/wd/hub
```
