from pages.main_page import MainPage
import allure

@allure.feature("Основной функционал")
@allure.story("Детали ингредиента")
@allure.title("Открытие модального окна с деталями ингредиента")
def test_open_ingredient_details_popup(driver):
    main = MainPage(driver)
    main.open_main()
    main.click_ingredient()

    assert main.is_ingredient_modal_opened()

@allure.feature("Основной функционал")
@allure.story("Детали ингредиента")
@allure.title("Закрытие модального окна деталей ингредиента по крестику")
def test_close_ingredient_details_popup_by_cross(driver):
    main = MainPage(driver)
    main.open_main()
    main.click_ingredient()
    assert main.is_ingredient_modal_opened()

    main.close_ingredient_modal()
    assert not main.is_ingredient_modal_opened()

@allure.feature("Основной функционал")
@allure.story("Добавление ингредиента")
@allure.title("Увеличение счётчика ингредиента после добавления в заказ")
def test_ingredient_counter_increases_after_adding(driver):
    main = MainPage(driver)
    main.open_main()

    before = main.get_ingredient_counter_value()
    main.add_ingredient_to_order()
    after = main.get_ingredient_counter_value()

    assert after == before + 1

@allure.feature("Основной функционал")
@allure.story("Оформление заказа")
@allure.title("Авторизованный пользователь может оформить заказ")
def test_authorized_user_can_place_order(driver, authorized_user):
    main = MainPage(driver).open_main()

    main.add_ingredient_to_order()
    main.place_order()

    order_number = main.get_order_number_from_modal()
    assert order_number.isdigit()

    main.close_order_modal()



