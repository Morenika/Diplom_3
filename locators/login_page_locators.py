# locators/login_page_locators.py
from selenium.webdriver.common.by import By


class LoginPageLocators:
    EMAIL_INPUT = (By.CSS_SELECTOR, "form.Auth_form__3qKeq input[type='text']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "form.Auth_form__3qKeq input[type='password']")
    SUBMIT_BUTTON = (By.XPATH, "//button[text()='Войти']")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//a[contains(@href,'/forgot-password')]")
    LOGIN_TITLE = (By.XPATH, "//div[contains(@class,'Auth_login')]//h2[normalize-space()='Вход']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Войти']")
    # Кнопка "глаз" (показать/скрыть пароль)
    PASSWORD_VISIBILITY_BUTTON = (By.CSS_SELECTOR,
        "div.input_type_password button, div.input_type_password svg, div.input_type_password .input__icon",)

    PASSWORD_INPUT = (By.CSS_SELECTOR, "div.input_type_password input",)

