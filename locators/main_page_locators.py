# locators/main_page_locators.py
from selenium.webdriver.common.by import By


class MainPageLocators:
    TITLE = (By.XPATH, "//h1[contains(.,'Соберите бургер')]")

    # Хедер
    ACCOUNT_BUTTON = (By.XPATH, "//p[normalize-space()='Личный Кабинет']/ancestor::a")
    FEED_LINK = (By.XPATH, "//p[normalize-space()='Лента Заказов']/ancestor::a")
    CONSTRUCTOR_LINK = (By.XPATH, "//p[normalize-space()='Конструктор']/ancestor::a")

    # ===== ИНГРЕДИЕНТЫ =====
    INGREDIENT_CARD = (By.XPATH, "//a[contains(@class,'BurgerIngredient')]")

    FIRST_NOT_BUN_INGREDIENT = (By.XPATH, "(//a[contains(@class,'BurgerIngredient')][not(.//*[contains(translate(., 'БУЛКА', 'булка'), 'булка')])])[1]")

    # Счётчик внутри карточки
    INGREDIENT_COUNTER_IN_CARD = (By.XPATH, ".//p[contains(@class,'counter__num')]")
    FIRST_NOT_BUN_COUNTER = (By.XPATH, "(//a[contains(@class,'BurgerIngredient')][not(.//*[contains(translate(., 'БУЛКА', 'булка'), 'булка')])])[1]" "//p[contains(@class,'counter__num')]")

    # Зона конструктора
    CONSTRUCTOR_DROP_AREA = (By.XPATH, "//section[contains(@class,'BurgerConstructor')]")

    # ===== ЗАКАЗ =====
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Оформить заказ']")

    # ===== МОДАЛКИ =====
    MODAL_OVERLAY = (By.XPATH, "//div[contains(@class,'Modal_modal_overlay')]")
    MODAL_CONTAINER = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]//button[contains(@class,'Modal_modal__close')]",)

    # Модалка ингредиента
    INGREDIENT_MODAL_TITLE = (By.XPATH, "//h2[normalize-space()='Детали ингредиента']")

    # Модалка заказа (номер заказа)
    ORDER_NUMBER = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]//h2[contains(@class,'text_type_digits-large')]",)
    
    # Булки
    BUN_CARD = (By.XPATH, "//h2[normalize-space()='Булки']/following::a[contains(@class,'BurgerIngredient')][1]")

    # Начинки: первая карточка в разделе "Начинки"
    FILLING_CARD = (By.XPATH, "//h2[normalize-space()='Начинки']/following::a[contains(@class,'BurgerIngredient')][1]")
