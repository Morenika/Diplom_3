# pages/password_recovery_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.password_recovery_page_locators import PasswordRecoveryPageLocators as Locators


class PasswordRecoveryPage(BasePage):
    def is_opened(self) -> bool:
        if "forgot-password" in self.driver.current_url:
            return True
        return self.is_visible(Locators.EMAIL_INPUT, timeout=5)

    def enter_email(self, email: str) -> None:
        self.type(Locators.EMAIL_INPUT, email, timeout=10)

    def click_restore(self) -> None:
        # нажать кнопку "Восстановить"
        self.safe_click(Locators.RESTORE_BUTTON, timeout=10)
        WebDriverWait(self.driver, 10).until(
            lambda d: "reset-password" in d.current_url or "forgot-password" not in d.current_url
        )
