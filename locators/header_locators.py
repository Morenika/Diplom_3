from selenium.webdriver.common.by import By


class HeaderLocators:
    # Кнопка "Личный кабинет"
    ACCOUNT_LINK = (By.CSS_SELECTOR, 'a[href="/account"]')

    # Ссылка "Лента заказов"
    FEED_LINK = (By.XPATH, "//a[@href='/feed' or normalize-space()='Лента заказов']")

    # Ссылка "Конструктор"
    CONSTRUCTOR_LINK = (By.XPATH, "//a[@href='/' or normalize-space()='Конструктор']")
