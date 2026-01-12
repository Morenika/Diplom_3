from pages.main_page import MainPage
from pages.feed_page import FeedPage
import allure

class TestNavigation:
    @allure.feature("Навигация")
    @allure.story("Лента заказов")
    @allure.title("Переход в ленту заказов из хедера")
    def test_open_feed_from_header(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.go_to_feed()
        assert "/feed" in driver.current_url

        feed = FeedPage(driver)
        assert feed.is_opened()

    @allure.feature("Навигация")
    @allure.story("Конструктор")
    @allure.title("Переход в конструктор из хедера")
    def test_open_constructor_from_header(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.go_to_constructor()
        assert driver.current_url == MainPage.URL or driver.current_url.endswith("/")
