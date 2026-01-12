# pages/main_page.py
from __future__ import annotations

import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class MainPageLocators:
    TITLE = (By.XPATH, "//h1[contains(.,'Соберите бургер')]")
    INGREDIENTS_SECTION = (By.XPATH, "//section[contains(@class,'BurgerIngredients')]")
    CONSTRUCTOR_AREA = (By.XPATH, "//section[contains(@class,'BurgerConstructor')]")

    # Ингредиенты: 1 булка + 1 начинка
    BUN_CARD = (
        By.XPATH,
        "//h2[normalize-space()='Булки']/following::a[contains(@class,'BurgerIngredient')][1]",
    )
    FILLING_CARD = (
        By.XPATH,
        "//h2[normalize-space()='Начинки']/following::a[contains(@class,'BurgerIngredient')][1]",
    )

    # Модалки (универсально)
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class,'Modal_modal_overlay')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class,'Modal_modal__close')]")

    # Заказ
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Оформить заказ']")
    ORDER_MODAL_TEXT = (By.XPATH, "//*[contains(normalize-space(),'идентификатор заказа')]")
    ORDER_NUMBER_IN_MODAL = (By.CSS_SELECTOR, "h2.text_type_digits-large")

    # Модалка ингредиента
    INGREDIENT_MODAL_TITLE = (By.XPATH, "//h2[normalize-space()='Детали ингредиента']")

    # Счётчик внутри карточки ингредиента (relative)
    COUNTER_IN_CARD = (By.XPATH, ".//p[contains(@class,'counter__num')]")



class MainPage(BasePage):
    URL = "https://stellarburgers.education-services.ru/"

    # ---------- helpers ----------
    @staticmethod
    def _digits(text: str) -> str:
        return "".join(ch for ch in (text or "") if ch.isdigit())

    def open_main(self):
        self.close_any_modal()
        self.open(self.URL)

        wait = WebDriverWait(self.driver, 30)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        wait.until(EC.presence_of_element_located(MainPageLocators.INGREDIENTS_SECTION))
        return self

    def close_any_modal(self) -> None:
        if self.is_visible(MainPageLocators.MODAL_OVERLAY, timeout=1):
            try:
                self.safe_click(MainPageLocators.MODAL_CLOSE_BUTTON, timeout=5)
            except Exception:
                self.press_esc()
            self.wait_invisible(MainPageLocators.MODAL_OVERLAY, timeout=15)

    def _html5_drag_and_drop(self, source, target) -> None:
        js = """
            const source = arguments[0];
            const target = arguments[1];
            const dataTransfer = new DataTransfer();

            function fire(type, elem) {
              const event = new DragEvent(type, { bubbles: true, cancelable: true, dataTransfer });
              elem.dispatchEvent(event);
            }

            fire('dragstart', source);
            fire('dragenter', target);
            fire('dragover', target);
            fire('drop', target);
            fire('dragend', source);
        """
        self.driver.execute_script(js, source, target)

    # ---------- navigation ----------
    def go_to_feed(self):
        self.close_any_modal()
        self.open(self.URL + "feed")
        return self

    def go_to_account(self):
        self.close_any_modal()
        self.open(self.URL + "account")
        return self

    def go_to_constructor(self):
        self.close_any_modal()
        self.open(self.URL)
        return self

    def go_to_profile_direct(self):
        self.close_any_modal()
        self.open(self.URL + "account/profile")
        return self

    # ---------- ingredients ----------
    def add_ingredient_to_order(self):
        self.find_visible(MainPageLocators.INGREDIENTS_SECTION, timeout=25)
        target = self.find_visible(MainPageLocators.CONSTRUCTOR_AREA, timeout=25)

        bun = self.find_visible(MainPageLocators.BUN_CARD, timeout=25)
        filling = self.find_visible(MainPageLocators.FILLING_CARD, timeout=25)

        self.scroll_into_view(bun)
        self.scroll_into_view(target)

        try:
            self._html5_drag_and_drop(bun, target)
        except Exception:
            ActionChains(self.driver).drag_and_drop(bun, target).perform()

        time.sleep(0.2)

        self.scroll_into_view(filling)
        self.scroll_into_view(target)

        try:
            self._html5_drag_and_drop(filling, target)
        except Exception:
            ActionChains(self.driver).drag_and_drop(filling, target).perform()

        time.sleep(0.2)
        return self

   # ---------- order ----------
    def place_order(self):
        self.close_any_modal()

    # клик
        self.safe_click(MainPageLocators.PLACE_ORDER_BUTTON, timeout=25)

    # модалка открылась
        self.find_visible(MainPageLocators.ORDER_MODAL_TEXT, timeout=30)
        self.find_visible(MainPageLocators.ORDER_NUMBER_IN_MODAL, timeout=30)


    def get_order_number_from_modal(self) -> str:
    # ждём, пока в модалке появится реальный номер (не 9999)
        def real_number_ready(drv):
            el = drv.find_element(*MainPageLocators.ORDER_NUMBER_IN_MODAL)
            txt = (el.get_attribute("textContent") or "").strip()
            digits = self._digits(txt)
            return bool(re.fullmatch(r"\d{4,}", digits)) and digits != "9999"

        WebDriverWait(self.driver, 120, poll_frequency=0.2).until(real_number_ready)

        el = self.find_visible(MainPageLocators.ORDER_NUMBER_IN_MODAL, timeout=10)
        txt = (el.get_attribute("textContent") or "").strip()
        digits = self._digits(txt)

        if not digits:
           raise AssertionError(f"Не удалось прочитать номер заказа. Текст: {txt!r}")
        return digits


    def close_order_modal(self):
        self.close_any_modal()
        return self

    def place_order_and_get_number(self) -> str:
        self.place_order()
        number = self.get_order_number_from_modal()
        self.close_order_modal()
        return number
    
    def click_ingredient(self):
        self.close_any_modal()
        card = self.find_visible(MainPageLocators.FILLING_CARD, timeout=20)
        self.scroll_into_view(card)
        card.click()
        return self

    def is_ingredient_modal_opened(self) -> bool:
        return self.is_visible(MainPageLocators.INGREDIENT_MODAL_TITLE, timeout=5)

    def close_ingredient_modal(self):
        if self.is_visible(MainPageLocators.MODAL_OVERLAY, timeout=2):
            self.safe_click(MainPageLocators.MODAL_CLOSE_BUTTON, timeout=10)
            self.wait_invisible(MainPageLocators.MODAL_OVERLAY, timeout=15)
        return self

    def get_ingredient_counter_value(self) -> int:
        card = self.find_visible(MainPageLocators.FILLING_CARD, timeout=20)
        counters = card.find_elements(*MainPageLocators.COUNTER_IN_CARD)
        if not counters:
            return 0
        return int(self._digits(counters[0].text) or 0)
    
    def is_title_visible(self) -> bool:
        return self.is_visible(MainPageLocators.TITLE, timeout=10)


