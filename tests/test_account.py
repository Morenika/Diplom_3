from pages.main_page import MainPage
from pages.profile_page import ProfilePage
from selenium.webdriver.support.ui import WebDriverWait
import allure

@allure.feature("Личный кабинет")
@allure.story("Переход в профиль")
@allure.title("Открытие страницы личного кабинета")
def test_open_account_page(driver, authorized_user):
    main = MainPage(driver)
    main.open_main()
    main.go_to_account()

    profile = ProfilePage(driver)

    assert profile.is_opened()

@allure.feature("Личный кабинет")
@allure.story("История заказов")
@allure.title("Переход в раздел истории заказов")
def test_open_order_history_from_account(driver, authorized_user):
    main = MainPage(driver)
    main.open_main()
    main.go_to_account()

    profile = ProfilePage(driver)
    profile.go_to_order_history()

    assert "/order-history" in driver.current_url

@allure.feature("Личный кабинет")
@allure.story("Выход из аккаунта")
@allure.title("Выход пользователя из личного кабинета")
def test_logout_from_account(driver, authorized_user):
    main = MainPage(driver)
    main.open_main()
    main.go_to_account()

    profile = ProfilePage(driver)
    assert profile.is_opened()

    profile.logout()
    assert "/login" in driver.current_url

