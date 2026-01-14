# conftest.py
import uuid
import pytest
import allure

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.api_client import StellarApi


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser for UI tests: chrome or firefox",
    )


@allure.step("Создаём драйвер для браузера: {browser_name}")
def create_driver(browser_name: str):
    browser_name = browser_name.lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(1280, 900)
        return driver

    if browser_name == "firefox":
        options = FirefoxOptions()
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1280, 900)
        return driver

    raise ValueError(f"Unsupported browser: {browser_name}")


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser")
    drv = create_driver(browser_name)
    yield drv
    with allure.step("Закрываем браузер"):
        drv.quit()


@pytest.fixture(scope="function")
def authorized_user(driver):
    api = StellarApi()

    email = f"test_{uuid.uuid4()}@mail.ru"
    password = "Password123"
    name = "Test User"

    register_response = api.register_user(email, password, name)
    assert register_response.status_code == 200

    login_response = api.login_user(email, password)
    assert login_response.status_code == 200

    access_token = None
    access_token = login_response.json()["accessToken"]

    try:
        from pages.main_page import MainPage
        from pages.login_page import LoginPage

        main = MainPage(driver)
        main.open_main()
        main.go_to_account()

        login_page = LoginPage(driver)
        login_page.login(email, password)

        main.go_to_profile_direct()

        yield {"email": email, "password": password, "access_token": access_token}
    finally:
        if access_token:
            api.delete_user(access_token)


@pytest.fixture
def user_order_number(driver, authorized_user):
    from pages.main_page import MainPage

    main = MainPage(driver)
    main.open_main()
    main.add_ingredient_to_order()
    number = main.place_order_and_get_number()
    return number

