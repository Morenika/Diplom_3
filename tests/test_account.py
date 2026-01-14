import allure

from pages.main_page import MainPage
from pages.profile_page import ProfilePage


@allure.feature("Личный кабинет")
class TestAccount:

    @allure.story("Переход в профиль")
    @allure.title("Открытие страницы личного кабинета")
    def test_open_account_page(self, driver, authorized_user):
        main = MainPage(driver)
        main.open_main()
        main.go_to_account()

        profile = ProfilePage(driver)
        assert profile.is_opened()

    @allure.story("История заказов")
    @allure.title("Переход в раздел истории заказов")
    def test_open_order_history_from_account(self, driver, authorized_user):
        main = MainPage(driver)
        main.open_main()
        main.go_to_account()

        profile = ProfilePage(driver)
        profile.go_to_order_history()
        assert profile.url_contains("/order-history")

    @allure.story("Выход из аккаунта")
    @allure.title("Выход пользователя из личного кабинета")
    def test_logout_from_account(self, driver, authorized_user):
        main = MainPage(driver)
        main.open_main()
        main.go_to_account()

        profile = ProfilePage(driver)
        assert profile.is_opened()

        profile.logout()
        assert profile.url_contains("/login")
