# locators/profile_page_locators.py

from selenium.webdriver.common.by import By


class ProfilePageLocators:
    PROFILE_ACTIVE_LINK = (By.XPATH, "//a[contains(@href,'/account/profile') and (@aria-current='page' or contains(@class,'active') or contains(@class,'Account_link_active'))]")
    ORDER_HISTORY_LINK = (By.XPATH, "//a[contains(@href,'/account/order-history')]")
    LOGOUT_BUTTON = (By.XPATH, "//nav[contains(@class,'Account_nav')]//button[normalize-space()='Выход']")
