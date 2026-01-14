from pages.main_page import MainPage
from pages.feed_page import FeedPage
from pages.profile_page import ProfilePage
import allure

@allure.feature("Лента заказов")
class TestOrderFeed:
     
    @allure.story("Детали заказа")
    @allure.title("Открытие модального окна с деталями заказа")
    def test_open_order_details_popup_from_feed(self, driver):
        main = MainPage(driver)
        main.open_main()
        main.go_to_feed()
        feed = FeedPage(driver)
        feed.click_order()

        assert feed.is_order_modal_opened()

    @allure.story("Детали заказа")
    @allure.title("Открытие модального окна с деталями заказа")
    def test_user_orders_are_visible_in_feed(self, driver, authorized_user, user_order_number):
        main = MainPage(driver)
        main.open_main()

        main.go_to_account()
        profile = ProfilePage(driver)
        profile.go_to_order_history()

        main.go_to_feed()
        feed = FeedPage(driver)

        assert feed.is_user_order_visible(user_order_number)

    @allure.story("Детали заказа")
    @allure.title("Открытие модального окна с деталями заказа")
    def test_total_done_counter_increases_after_order(self, driver, authorized_user):
        main = MainPage(driver)
        main.open_main()
        main.go_to_feed()

        feed = FeedPage(driver)
        before = feed.get_total_done_counter()

        main.open_main()
        main.add_ingredient_to_order()
        main.place_order()

        main.go_to_feed()
        feed = FeedPage(driver)
        after = feed.get_total_done_counter()

        assert after > before

    @allure.story("Детали заказа")
    @allure.title("Открытие модального окна с деталями заказа")
    def test_today_done_counter_increases_after_order(self, driver, authorized_user):
        main = MainPage(driver)
        main.open_main()
        main.go_to_feed()

        feed = FeedPage(driver)
        before = feed.get_today_done_counter()

        main.open_main()
        main.add_ingredient_to_order()
        main.place_order()

        main.go_to_feed()
        feed = FeedPage(driver)
        after = feed.get_today_done_counter()

        assert after > before
        
    @allure.story("Детали заказа")
    @allure.title("Открытие модального окна с деталями заказа")
    def test_new_order_number_appears_in_progress(self, driver, authorized_user):
        main = MainPage(driver)
        main.open_main()

        main.add_ingredient_to_order()
        main.place_order()
        order_number = main.get_order_number_from_modal()

        main.go_to_feed()
        feed = FeedPage(driver)

        assert feed.is_order_in_progress(order_number)
