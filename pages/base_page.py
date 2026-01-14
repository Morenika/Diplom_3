# pages/base_page.py
from __future__ import annotations
import allure

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open(self, url: str):
        self.driver.get(url)

    def find_visible(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_clickable(self, locator, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def click(self, locator, timeout: int = 10):
        self.find_clickable(locator, timeout).click()

    def is_visible(self, locator, timeout: int = 2) -> bool:
        try:
            self.find_visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def wait_invisible(self, locator, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))

    def wait_url_contains(self, part: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(part))

    def wait_url_not_contains(self, part: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until_not(EC.url_contains(part))

    def wait_url_to_be(self, url: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.url_to_be(url))

    def send_keys(self, locator, text: str, timeout: int = 10):
        el = self.find_visible(locator, timeout)
        el.clear()
        el.send_keys(text)

    def type(self, locator, text: str, timeout: int = 10):
        self.send_keys(locator, text, timeout)

    def scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def press_esc(self):
        try:
            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        except Exception:
            pass

    def safe_click(self, locator, timeout: int = 15):
        overlay = ("xpath", "//div[contains(@class,'Modal_modal_overlay')]")

        last_exc = None
        for _ in range(3):
            try:
                el = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
                self.scroll_into_view(el)
                el.click()
                return
            except (ElementClickInterceptedException, StaleElementReferenceException) as e:
                last_exc = e
                try:
                    WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(overlay))
                except Exception:
                    pass

        if last_exc:
            raise last_exc
        
    @allure.step("Проверить, что URL содержит: {part}")
    def url_contains(self, part: str, timeout: int = 10) -> bool:
        try:
            self.wait_url_contains(part, timeout)
            return True
        except TimeoutException:
            return False

