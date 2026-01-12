# pages/login_page.py
from __future__ import annotations
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):
    def is_opened(self) -> bool:
        return self.is_visible(LoginPageLocators.LOGIN_TITLE, timeout=10)

    def login(self, email: str, password: str) -> None:
        self.find_visible(LoginPageLocators.LOGIN_TITLE, timeout=15)

        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)

        pass_el = self.find_visible(LoginPageLocators.PASSWORD_INPUT, timeout=5)

        pass_el.send_keys(Keys.ENTER)

        self.wait_url_not_contains("/login", timeout=20)

    def go_to_forgot_password(self) -> None:
        overlay = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")
        if self.is_visible(overlay, timeout=1):
           self.wait_invisible(overlay, timeout=10)

        self.safe_click(LoginPageLocators.FORGOT_PASSWORD_LINK, timeout=15)
        self.wait_url_contains("/forgot-password", timeout=10)


    def toggle_password_visibility(self) -> None:
        btn = (By.CSS_SELECTOR, "div.input_type_password button")
        if self.is_visible(btn, timeout=1):
            self.safe_click(btn, timeout=10)
        else:
            self.safe_click(LoginPageLocators.PASSWORD_VISIBILITY_BUTTON, timeout=10)

    def is_password_field_active(self) -> bool:
        el = self.find_visible(LoginPageLocators.PASSWORD_INPUT, timeout=5)
        return (el.get_attribute("type") or "").lower() == "text"
