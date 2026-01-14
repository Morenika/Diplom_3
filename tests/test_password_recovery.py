from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.password_recovery_page import PasswordRecoveryPage
from pages.reset_password_page import ResetPasswordPage
import allure

@allure.feature("Восстановление пароля")
class TestPasswordRecovery:

    @allure.story("Навигация")
    @allure.title("Переход на страницу восстановления пароля по кнопке")
    def test_open_password_recovery_page(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.go_to_account()  

        login = LoginPage(driver)
        login.go_to_forgot_password()

        recovery = PasswordRecoveryPage(driver)
        assert recovery.is_opened()

    @allure.story("Отправка формы восстановления")
    @allure.title("Переход на страницу восстановления и отправка email")
    def test_restore_password_by_email(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.go_to_account()

        login = LoginPage(driver)
        assert login.is_opened()
        login.go_to_forgot_password()

        recovery = PasswordRecoveryPage(driver)
        recovery.enter_email("test@test.ru")
        recovery.click_restore()

        reset = ResetPasswordPage(driver)
        assert reset.is_opened()


    @allure.story("Активация поля пароля")
    @allure.title("Поле пароля становится активным при клике на иконку глаза")
    def test_password_field_becomes_active_on_visibility_toggle(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.go_to_account()

        login = LoginPage(driver)
        assert login.is_opened()
        login.go_to_forgot_password()

        recovery = PasswordRecoveryPage(driver)
        recovery.enter_email("test@test.ru")
        recovery.click_restore()

        reset = ResetPasswordPage(driver)
        assert reset.is_opened()

        reset.toggle_password_visibility()
        assert reset.is_password_field_active()

