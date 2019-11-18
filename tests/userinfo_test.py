import unittest
import os
import configparser
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from pages.auth_page import AuthPage
from pages.userinfo_page import UserinfoPage
from helpers import *

class UserinfoTest(unittest.TestCase):
    config = configparser.ConfigParser()

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        self.config.read('test_data.ini')


    def tearDown(self):
        self.driver.quit()

    def test_tick_in_time_zone(self):   
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.uncheck_town()
        userinfo_form.get_town_selector()

    def test_phone_redirect(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        new_window_url = userinfo_form.get_url_phone_link()
        self.driver.get(new_window_url)

        self.assertEqual(self.driver.current_url, new_window_url)

    def test_load_image(self):        
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.load_image()
        userinfo_form.get_save_avatar_button()
        userinfo_form.get_cancel_avatar_button()
        
    def test_cancel_changed_data(self):
        SURNAME_NEW_VALUE = 'new surname'

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        old_surname_value = userinfo_form.get_surname_value()
        userinfo_form.set_surname(SURNAME_NEW_VALUE)
        userinfo_form.cancel()
        userinfo_page.open()
        new_surname_value = userinfo_form.get_surname_value()
        self.assertEqual(old_surname_value, new_surname_value)

    def test_error_saving(self):
        TOP_MESSAGE = 'Не заполнены необходимые поля'
        SURNAME_ERROR = 'Заполните обязательное поле'
        EMPTY_SURNAME = ''

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.set_surname(EMPTY_SURNAME)
        userinfo_form.save()
        self.assertEqual(TOP_MESSAGE, userinfo_form.get_top_message())
        self.assertEqual(SURNAME_ERROR, userinfo_form.get_surname_message())

    def test_gender(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        unselected_gender_before = userinfo_form.get_unselected_gender()
        unselected_gender_before_id = unselected_gender_before.id
        unselected_gender_before.click()
        userinfo_form.save()

        userinfo_page.open()
        userinfo_form = userinfo_page.form

        unselected_gender_after = userinfo_form.get_unselected_gender()
        unselected_gender_after_id = unselected_gender_after.id
        self.assertNotEqual(unselected_gender_before_id, unselected_gender_after_id)

    def test_long_name(self):
        LONG_SURNAME = f'{"very" * 10} long'
        TOP_MESSAGE = 'Некоторые поля заполнены неверно'
        SURNAME_ERROR = 'Поле не может содержать специальных символов и должно иметь длину от 1 до 40 символов.'
        
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form
        
        userinfo_form.set_surname(LONG_SURNAME)
        userinfo_form.save()
        self.assertEqual(TOP_MESSAGE, userinfo_form.get_top_message())
        self.assertEqual(SURNAME_ERROR, userinfo_form.get_surname_message())

    def test_suggest_town(self):
        TOWN_PREFIX = 'Мос' 
        SUGGEST_LIST = [
            'Москва, Россия',
            'Московский, Московская обл., Россия',
            'Мосальск, Калужская обл., Россия'
        ]

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.set_town(TOWN_PREFIX)
        userinfo_form.wait_for_last_suggest(SUGGEST_LIST[-1])
        self.assertEqual(SUGGEST_LIST, userinfo_form.get_suggests_for_town()) 

    def test_wrong_town(self):
        WRONG_TOWN_NAME = 'qwertyuiop'
        TOP_MESSAGE = 'Некоторые поля заполнены неверно'
        TOWN_ERROR = 'Проверьте название города'

        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.set_town(WRONG_TOWN_NAME)
        userinfo_form.wait_for_suggests_invisible()
        userinfo_form.save()
        self.assertEqual(TOP_MESSAGE, userinfo_form.get_top_message())
        self.assertEqual(TOWN_ERROR, userinfo_form.get_town_message())             

    def test_correct_input(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.input_firstname(randomString())
        userinfo_form.input_lastname(randomString())
        userinfo_form.input_nickname(randomString())

        userinfo_form.click_submit_button()
        userinfo_form.wait_for_ok_after_submit()

    def test_image_upload(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.input_test_image()

        userinfo_form.click_submit_button()
        userinfo_form.wait_for_ok_after_submit()

    def test_logout(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.open_settings_in_new_window()
        userinfo_form.wait_for_ok_after_submit()

        userinfo_form.click_logout_button()
        userinfo_form.wait_for_logout()

        userinfo_form.switch_to_window(0)
        userinfo_form.refresh_page()
        userinfo_form.match_to_login_URI()


    def test_date_lists(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.click_on_day_input()
        userinfo_form.click_on_day_child_input()
        userinfo_form.click_on_month_input()
        userinfo_form.click_on_month_child_input()
        userinfo_form.click_on_year_input()
        userinfo_form.click_on_year_child_input()

        userinfo_form.click_submit_button()
        userinfo_form.wait_for_ok_after_submit()

    def test_open_help(self):
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.click_on_help()
        userinfo_form.switch_to_window(1)
        userinfo_form.wait_for_help()    