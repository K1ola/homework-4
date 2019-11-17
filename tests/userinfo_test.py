import unittest
import os
import configparser
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote
from pages.auth_page import AuthPage
from pages.userinfo_page import UserinfoPage
from helpers import *

class UserinfoTest(unittest.TestCase):
    USEREMAIL = 'yekaterina.kirillova.1998@bk.ru'
    PASSWORD = 'qwerYtuarRyYY12'
    config = configparser.ConfigParser()

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')

        self.driver = webdriver.Chrome()
        self.config.read('test_data.ini')


    def tearDown(self):
        self.driver.quit()

    # def test_tick_in_time_zone(self):   
    #     auth_page = AuthPage(self.driver)
    #     auth_page.open()
    #     auth_page.authorize()

    #     userinfo_page = UserinfoPage(self.driver)
    #     userinfo_page.open()
    #     userinfo_form = userinfo_page.form

    #     userinfo_form.uncheck_town()
    #     userinfo_form.get_town_selector()

    # def test_phone_redirect(self):
    #     auth_page = AuthPage(self.driver)
    #     auth_page.open()
    #     auth_page.authorize()

    #     userinfo_page = UserinfoPage(self.driver)
    #     userinfo_page.open()
    #     userinfo_form = userinfo_page.form

    #     new_window_url = userinfo_form.get_url_phone_link()
    #     self.driver.get(new_window_url)

    #     self.assertEqual(self.driver.current_url, new_window_url)
        

    def test_load_image(self):
        IMAGE = self.config['DEFAULT']['ImageFile']
        
        auth_page = AuthPage(self.driver)
        auth_page.open()
        auth_page.authorize()

        userinfo_page = UserinfoPage(self.driver)
        userinfo_page.open()
        userinfo_form = userinfo_page.form

        userinfo_form.load_image(IMAGE)
        userinfo_form.get_save_avatar_button()
        userinfo_form.get_cancel_avatar_button()
        
    # def test_do_snapshot(self):
    #     auth_page = AuthPage(self.driver)
    #     auth_page.open()
    #     auth_page.authorize()

    #     userinfo_page = UserinfoPage(self.driver)
    #     userinfo_page.open()
    #     userinfo_form = userinfo_page.form

    #     userinfo_form.dismiss_snapshot_request()
   
    # def test_cancel_changed_data(self):
    #     SURNAME_NEW_VALUE = 'new surname'

    #     auth_page = AuthPage(self.driver)
    #     auth_page.open()
    #     auth_page.authorize()

    #     userinfo_page = UserinfoPage(self.driver)
    #     userinfo_page.open()
    #     userinfo_form = userinfo_page.form

    #     old_surname_value = userinfo_form.get_surname_value()
    #     userinfo_form.set_surname(SURNAME_NEW_VALUE)
    #     userinfo_form.cancel()
    #     userinfo_page.open()
    #     new_surname_value = userinfo_form.get_surname_value()
    #     self.assertEqual(old_surname_value, new_surname_value)

    # def test_error_saving(self):
    #     TOP_MESSAGE = 'Не заполнены необходимые поля'
    #     SURNAME_ERROR = 'Заполните обязательное поле'

    #     auth_page = AuthPage(self.driver)
    #     auth_page.open()
    #     auth_page.authorize()

    #     userinfo_page = UserinfoPage(self.driver)
    #     userinfo_page.open()
    #     userinfo_form = userinfo_page.form

    #     userinfo_form.set_surname('')
    #     userinfo_form.save()
    #     self.assertEqual(TOP_MESSAGE, userinfo_form.get_top_message())
    #     self.assertEqual(SURNAME_ERROR, userinfo_form.get_surname_message())

