# locators/password_recovery_page_locators.py

from selenium.webdriver.common.by import By


class PasswordRecoveryPageLocators:
    TITLE = (By.XPATH, "//*[contains(.,'Восстановление пароля') or contains(.,'Восстановить пароль')]")
    EMAIL_INPUT = (By.XPATH, "//label[contains(.,'Email')]/following-sibling::input")
    RESTORE_BUTTON = (By.XPATH, "//button[contains(.,'Восстановить') or contains(.,'Восстановить пароль')]")
