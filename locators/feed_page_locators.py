# locators/feed_page_locators.py
from selenium.webdriver.common.by import By


class FeedPageLocators:
    # Страница ленты
    TITLE = (By.XPATH, "//*[self::h1 or self::h2][contains(normalize-space(.),'Лента')]")

    FIRST_ORDER = (By.XPATH, "(//a[contains(@class,'OrderHistory_link')])[1]")

    # Модалка деталей заказа
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class,'Modal_modal_overlay')]")
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]")
    MODAL_CLOSE = (By.XPATH, "//button[contains(@class,'Modal_modal__close')]")

    ORDER_MODAL_ANY_TEXT = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]//*[contains(.,'Состав') or contains(.,'Cостав') or contains(.,'Детали')]",)

    # Счётчики выполнено
    TOTAL_DONE_VALUE = (By.XPATH,
        "//*[contains(.,'Выполнено за все время')]/following-sibling::*[1]//*[contains(@class,'text_type_digits-large')]"
        "|//*[contains(.,'Выполнено за все время')]/..//*[contains(@class,'text_type_digits-large')]",)
    TODAY_DONE_VALUE = (By.XPATH,
        "//*[contains(.,'Выполнено за сегодня')]/following-sibling::*[1]//*[contains(@class,'text_type_digits-large')]"
        "|//*[contains(.,'Выполнено за сегодня')]/..//*[contains(@class,'text_type_digits-large')]",)

    # Колонки "Готовы" / "В работе" (ищем номер заказа внутри соответствующего блока)
    IN_PROGRESS_COLUMN = (By.XPATH, "//*[normalize-space()='В работе']/ancestor::*[self::section or self::div][1]")
