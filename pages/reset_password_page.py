from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ResetPasswordLocators:
    PASSWORD_INPUT_ANY = (
        By.XPATH,
        "//label[normalize-space()='Пароль']/following-sibling::input"
        "|//label[contains(normalize-space(),'Пароль')]/following-sibling::input"
        "|//input[@name='password']"
        "|//input[contains(@class,'input__textfield')]",
    )

    # Кнопка/иконка глаз
    VISIBILITY_BTN = (
        By.CSS_SELECTOR,
        "div.input_type_password button, div.input_type_password svg, .input__icon, button[type='button'] svg",
    )


class ResetPasswordPage(BasePage):
    def is_opened(self) -> bool:
        return "reset-password" in self.driver.current_url

    def toggle_password_visibility(self) -> None:
        overlay = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")
        if self.is_visible(overlay, timeout=1):
            self.wait_invisible(overlay, timeout=10)

        try:
            self.safe_click(ResetPasswordLocators.VISIBILITY_BTN, timeout=10)
        except Exception:
            el = self.find_visible(ResetPasswordLocators.VISIBILITY_BTN, timeout=10)
            self.driver.execute_script("arguments[0].click();", el)

    def is_password_field_active(self) -> bool:
        inputs = self.driver.find_elements(*ResetPasswordLocators.PASSWORD_INPUT_ANY)
        if not inputs:
            raise AssertionError("Не найдено поле пароля на странице reset-password")

        inp = next((el for el in inputs if el.is_displayed()), inputs[0])

        in_focus = self.driver.switch_to.active_element == inp
        type_is_text = (inp.get_attribute("type") or "").lower() == "text"

        parent_class = ""
        try:
            parent_class = (inp.find_element(By.XPATH, "./..").get_attribute("class") or "").lower()
        except Exception:
            pass

        parent_active = ("active" in parent_class) or ("focused" in parent_class)

        return in_focus or type_is_text or parent_active
