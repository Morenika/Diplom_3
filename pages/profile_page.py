# pages/profile_page.py
from __future__ import annotations

import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from locators.profile_page_locators import ProfilePageLocators as Locators

from pages.base_page import BasePage


class ProfilePageInternalLocators:
    ORDER_HISTORY_LINK = (By.CSS_SELECTOR, "a[href='/account/order-history']")
    MODAL_OVERLAY = (By.CSS_SELECTOR, "div[class*='Modal_modal_overlay']")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")


class ProfilePage(BasePage):
    BASE_URL = "https://stellarburgers.education-services.ru/"

    def _kill_overlay_if_any(self, timeout: int = 8) -> None:
        end = time.time() + timeout

        while time.time() < end:
            overlays = self.driver.find_elements(*ProfilePageInternalLocators.MODAL_OVERLAY)
            if not overlays:
                return

            closes = self.driver.find_elements(*ProfilePageInternalLocators.MODAL_CLOSE_BUTTON)
            if closes:
                try:
                    closes[0].click()
                except Exception:
                    try:
                        self.js_click(closes[0])
                    except Exception:
                        pass
            else:
                try:
                    self.press_esc()
                except Exception:
                    pass

            try:
                WebDriverWait(self.driver, 2).until(
                    lambda d: len(d.find_elements(*ProfilePageInternalLocators.MODAL_OVERLAY)) == 0
                )
                return
            except TimeoutException:
                time.sleep(0.2)


    def go_to_order_history(self):
        self._kill_overlay_if_any(timeout=8)

        self.open(self.BASE_URL + "account/order-history")

        self._kill_overlay_if_any(timeout=6)
        return self
    
    def is_opened(self) -> bool:
        return self.is_visible(Locators.PROFILE_ACTIVE_LINK, timeout=10)

    def logout(self) -> None:
        self._kill_overlay_if_any(timeout=6)
        self.safe_click(Locators.LOGOUT_BUTTON, timeout=10)
        self.wait_url_contains("/login", timeout=15)

