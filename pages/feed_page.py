# pages/feed_page.py
from __future__ import annotations

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class FeedPageLocators:
    # Карточки заказов в ленте
    ORDER_CARDS = (By.CSS_SELECTOR, "a[class*='OrderHistory_link'][href^='/feed/']")

    # Модальное окно
    MODAL_CONTAINER = (By.CSS_SELECTOR, "div[class*='Modal_modal__container']")
    MODAL_CONTENT = (By.CSS_SELECTOR, "div[class*='Modal_modal__contentBox']")
    MODAL_CLOSE = (By.CSS_SELECTOR, "button[class*='Modal_modal__close']")

    # Номер заказа внутри модалки
    MODAL_ORDER_NUMBER = (By.CSS_SELECTOR, "div[class*='Modal'] p.text_type_digits-default")

    ORDER_DETAILS_TITLE = (
        By.XPATH,
        "//*[self::h1 or self::h2][contains(normalize-space(),'Детали заказа')]",
    )

    # Счётчики
    TOTAL_DONE = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за все время:']/following-sibling::p[contains(@class,'OrderFeed_number')]",
    )
    TODAY_DONE = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p[contains(@class,'OrderFeed_number')]",
    )

    # Номер заказа внутри карточки
    ORDER_NUMBER_IN_CARD = (By.CSS_SELECTOR, "p.text_type_digits-default")


class FeedPage(BasePage):
    URL = "https://stellarburgers.education-services.ru/feed"

    # --------- utils ----------
    @staticmethod
    def _digits(text: str) -> str:
        return "".join(ch for ch in (text or "") if ch.isdigit())

    @staticmethod
    def _int(text: str) -> int:
        d = FeedPage._digits(text)
        return int(d) if d else 0

    def open_feed(self):
        self.open(self.URL)
        self.find_visible(FeedPageLocators.ORDER_CARDS, timeout=30)
        return self
    
    def is_opened(self) -> bool:
        if "/feed" not in self.driver.current_url:
            return False
        return self.is_visible(FeedPageLocators.ORDER_CARDS, timeout=10)


    def click_order(self, index: int = 0):
        self.find_visible(FeedPageLocators.ORDER_CARDS, timeout=30)

        orders = self.driver.find_elements(*FeedPageLocators.ORDER_CARDS)
        if len(orders) <= index:
            raise AssertionError(f"В ленте нет заказа с индексом {index}. Найдено: {len(orders)}")

        order = orders[index]
        href = order.get_attribute("href") or ""
        m = re.search(r"/feed/(\d+)", href)
        order_id = m.group(1) if m else ""
        expected_url_part = f"/feed/{order_id}" if order_id else ""

        self.scroll_into_view(order)

        try:
            WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(order))
            order.click()
        except Exception:
            self.js_click(order)

        def opened(d):
            url_ok = bool(expected_url_part) and (expected_url_part in d.current_url)
            modal_exists = (
                len(d.find_elements(*FeedPageLocators.MODAL_CONTAINER)) > 0
                or len(d.find_elements(*FeedPageLocators.MODAL_CONTENT)) > 0
                or len(d.find_elements(*FeedPageLocators.MODAL_CLOSE)) > 0
                or len(d.find_elements(*FeedPageLocators.MODAL_ORDER_NUMBER)) > 0
            )
            return url_ok or modal_exists

        WebDriverWait(self.driver, 30).until(opened)
        time.sleep(0.2)  
        return self

    # --------- assertions / checks ----------
    def is_order_modal_opened(self) -> bool:
        if (
            len(self.driver.find_elements(*FeedPageLocators.MODAL_CONTAINER)) > 0
            or len(self.driver.find_elements(*FeedPageLocators.MODAL_CONTENT)) > 0
            or len(self.driver.find_elements(*FeedPageLocators.MODAL_CLOSE)) > 0
            or len(self.driver.find_elements(*FeedPageLocators.MODAL_ORDER_NUMBER)) > 0
        ):
            return True

        if re.search(r"/feed/\d+$", self.driver.current_url):
            return True

        return False

    def close_order_details_modal(self):
        if len(self.driver.find_elements(*FeedPageLocators.MODAL_CLOSE)) > 0:
            try:
                self.safe_click(FeedPageLocators.MODAL_CLOSE, timeout=5)
            except Exception:
                self.press_esc()
            self.wait_invisible(FeedPageLocators.MODAL_CONTAINER, timeout=10)
        return self

    def get_order_number_from_modal(self) -> str:
        el = self.find_visible(FeedPageLocators.MODAL_ORDER_NUMBER, timeout=10)
        return self._digits(el.text)

    # --------- counters ----------
    def get_total_done_counter(self) -> int:
        el = self.find_visible(FeedPageLocators.TOTAL_DONE, timeout=30)
        return self._int(el.text)

    def get_today_done_counter(self) -> int:
        el = self.find_visible(FeedPageLocators.TODAY_DONE, timeout=30)
        return self._int(el.text)

    # --------- search ----------
    def is_user_order_visible(self, order_number: str) -> bool:
        target = self._digits(order_number)
        if not target:
            return False

        target7 = target.zfill(7)

        self.find_visible(FeedPageLocators.ORDER_CARDS, timeout=30)
        orders = self.driver.find_elements(*FeedPageLocators.ORDER_CARDS)

        for a in orders:
            try:
                num_el = a.find_element(*FeedPageLocators.ORDER_NUMBER_IN_CARD)
                digits = self._digits(num_el.text)
                if digits == target7:
                    return True
            except Exception:
                continue

        return False

    def is_order_in_progress(self, order_number: str, timeout: int = 90) -> bool:
        raw = self._digits(order_number)
        if not raw:
            return False

        variants = {raw, raw.lstrip("0") or "0", raw.zfill(7)}

        # li в колонке "В работе"
        xpath = (
            "//p[normalize-space()='В работе:']"
            "/following-sibling::ul[contains(@class,'OrderFeed_orderList')][1]"
            + "".join([f"//li[normalize-space()='{v}'] | " for v in variants]).rstrip(" | ")
        )
        locator = (By.XPATH, xpath)

        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except Exception:
            return False
