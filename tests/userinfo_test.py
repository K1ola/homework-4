import unittest
import os
import configparser
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from pages.auth_page import AuthPage
from pages.userinfo_page import UserinfoPage

class UserinfoTest(unittest.TestCase):
    userinfo_page = None
    userinfo_form = None

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        self.userinfo_page = UserinfoPage(self.driver)
        self.userinfo_page.open()
        self.userinfo_form = self.userinfo_page.form

    def tearDown(self):
        self.userinfo_form.click_logout_button()
        # self.userinfo_form.wait_for_logout()
        self.driver.quit()

    def test_check_timezone(self):  
        TIMEZONE_SELECT_LIST_VALUE = '(GMT+03:00) Москва, Санкт-Петербург' 

        self.userinfo_form.uncheck_tick()
        self.userinfo_form.wait_for_timezone_selector_first_value(TIMEZONE_SELECT_LIST_VALUE)
        self.assertEqual(TIMEZONE_SELECT_LIST_VALUE, self.userinfo_form.get_timezone_selector_first_value())

    def test_image_preview_buttons(self):        
        self.userinfo_form.load_image()
        self.userinfo_form.get_save_avatar_button()
        self.userinfo_form.get_cancel_avatar_button()
        
    def test_cancel_changed_data(self):
        SURNAME_NEW_VALUE = 'new surname'

        old_surname_value = self.userinfo_form.get_surname_value()
        self.userinfo_form.set_surname(SURNAME_NEW_VALUE)
        self.userinfo_form.cancel()
        userinfo_page.open()
        new_surname_value = self.userinfo_form.get_surname_value()
        self.assertEqual(old_surname_value, new_surname_value)

    def test_save_empty_field(self):
        TOP_MESSAGE = 'Не заполнены необходимые поля'
        SURNAME_ERROR = 'Заполните обязательное поле'
        EMPTY_SURNAME = ''

        self.userinfo_form.set_surname(EMPTY_SURNAME)
        self.userinfo_form.save()
        self.assertEqual(TOP_MESSAGE, self.userinfo_form.get_top_message())
        self.assertEqual(SURNAME_ERROR, self.userinfo_form.get_surname_message())

    def test_gender(self):
        unselected_gender_before = self.userinfo_form.get_unselected_gender()
        unselected_gender_before_id = unselected_gender_before.id
        unselected_gender_before.click()
        self.userinfo_form.save()

        userinfo_page.open()
        self.userinfo_form = userinfo_page.form

        unselected_gender_after = self.userinfo_form.get_unselected_gender()
        unselected_gender_after_id = unselected_gender_after.id
        self.assertNotEqual(unselected_gender_before_id, unselected_gender_after_id)

    def test_long_name(self):
        LONG_SURNAME = f'{"very" * 10} long'
        TOP_MESSAGE = 'Некоторые поля заполнены неверно'
        SURNAME_ERROR = 'Поле не может содержать специальных символов и должно иметь длину от 1 до 40 символов.'
        
        self.userinfo_form.set_surname(LONG_SURNAME)
        self.userinfo_form.save()
        self.assertEqual(TOP_MESSAGE, self.userinfo_form.get_top_message())
        self.assertEqual(SURNAME_ERROR, self.userinfo_form.get_surname_message())

    def test_suggest_town(self):
        TOWN_PREFIX = 'Мос' 
        SUGGEST_LIST = [
            'Москва, Россия',
            'Московский, Московская обл., Россия',
            'Мосальск, Калужская обл., Россия'
        ]

        self.userinfo_form.set_town(TOWN_PREFIX)
        self.userinfo_form.wait_for_last_suggest(SUGGEST_LIST[-1])
        self.assertEqual(SUGGEST_LIST, self.userinfo_form.get_suggests_for_town()) 

    def test_wrong_town(self):
        WRONG_TOWN_NAME = 'qwertyuiop'
        TOP_MESSAGE = 'Некоторые поля заполнены неверно'
        TOWN_ERROR = 'Проверьте название города'

        self.userinfo_form.set_town(WRONG_TOWN_NAME)
        self.userinfo_form.wait_for_suggests_invisible()
        self.userinfo_form.save()
        self.assertEqual(TOP_MESSAGE, self.userinfo_form.get_top_message())
        self.assertEqual(TOWN_ERROR, self.userinfo_form.get_town_message())             

    def test_correct_input(self):
        self.userinfo_form.input_firstname(randomString())
        self.userinfo_form.input_lastname(randomString())
        self.userinfo_form.input_nickname(randomString())

        self.userinfo_form.save()

    def test_image_upload(self):
        self.userinfo_form.input_test_image()
        self.userinfo_form.save()

    def test_logout(self):
        self.userinfo_form.open_settings_in_new_window()
        self.userinfo_form.wait_for_ok_after_submit()

        self.userinfo_form.click_logout_button()
        self.userinfo_form.wait_for_logout()

        self.userinfo_form.switch_to_window(0)
        self.userinfo_form.refresh_page()
        self.userinfo_form.match_to_login_URI()


    def test_date_lists(self):
        DAY_CHILD_INPUT = 20
        MONTH_CHILD_INPUT = 12
        YEAR_CHILD_INPUT = 1996

        self.userinfo_form.click_on_day_input()
        self.userinfo_form.click_on_day_child_input(DAY_CHILD_INPUT)
        self.userinfo_form.click_on_month_input()

        self.userinfo_form.click_on_month_child_input(MONTH_CHILD_INPUT)
        self.userinfo_form.click_on_year_input()
        
        self.userinfo_form.click_on_year_child_input(YEAR_CHILD_INPUT)

        self.userinfo_form.save()
        self.userinfo_page.open()
