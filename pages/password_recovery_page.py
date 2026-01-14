# pages/password_recovery_page.py
import allure

from pages.base_page import BasePage
from locators.password_recovery_page_locators import PasswordRecoveryPageLocators as Locators


class PasswordRecoveryPage(BasePage):

    @allure.step("Проверить: открыта страница восстановления пароля")
    def is_opened(self) -> bool:
        # 1) предпочтительно проверяем URL (без driver.current_url)
        if self.url_contains("/forgot-password", timeout=5):
            return True
        # 2) fallback: проверяем наличие поля email
        return self.is_visible(Locators.EMAIL_INPUT, timeout=5)

    @allure.step("Ввести email для восстановления: {email}")
    def enter_email(self, email: str) -> None:
        self.type(Locators.EMAIL_INPUT, email, timeout=10)

    @allure.step("Нажать кнопку 'Восстановить'")
    def click_restore(self) -> None:
        self.safe_click(Locators.RESTORE_BUTTON, timeout=10)
        # ждём перехода на reset-password
        if not self.url_contains("/reset-password", timeout=15):
            raise AssertionError("Не произошёл переход на страницу /reset-password после отправки формы")
