import os
import time

from pages.default_page import DefaultPage, Component
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from helpers import wait, wait_redirect, wait_for_element_by_selector, wait_for_element_by_xpath, wait_for_text_by_xpath, wait_for_text_by_selector


class UserinfoPage(DefaultPage):
    URL = 'https://e.mail.ru/settings/userinfo'

    @property
    def form(self):
        return UserinfoForm(self.driver)

class UserinfoForm(Component):
    TOWN = 'input[name="your_town"]'
    LAST_NAME = 'input[name="LastName"]'            
    SAVE = 'div.form__actions__inner button[type="submit"]'
    CANCEL = 'body div.form__actions.form__actions_floating a'
    TOP_MESSAGE = 'div.content__page span'
    TOWN_ERROR = 'input[name="your_town"] ~ .form__message.form__message_error'
    LAST_NAME_ERROR = '#formPersonal div.form__message_error'
    MAKE_SNAPSHOT = '#js-edit-avatar button.js-camera'
    LOAD_IMAGE = '#js-edit-avatar input[name="avatar"]'
    SAVE_AVATAR_TEXT = '#MailRuConfirm div[data-fire="save"] .btn__text'
    CANCEL_AVATAR_TEXT = '#MailRuConfirm div[data-fire="cancel"] .btn__text'
    PHONE_LINK = '#phonesContainer a.js-click-security-recovery'
    TIMEZONE_TICK = 'input[name=UseAutoTimezone]'
    TIMEZONE_SELECTOR = 'select[name=TimeZone]'
    TIMEZONE_SELECTOR_DIV = 'div.js-timezone .form__select__box__text'
    SUGGESTS = '//*[@class="content__page"]/descendant::span[@class="div_inner ac-items form__field__suggest__inner"]'
    SUGGESTS_ITEM = '//form[@id="formPersonal"]//*[@class="form__field__suggest__item"]'
    GENDER_MALE = 'label[for="man1"] input'
    GENDER_FEMALE = 'label[for="man2"] input'

    FIRST_NAME = '#FirstName'
    NICK_NAME = '#NickName'

    IMAGE_AVATAR = '#js-edit-avatar .form__row__avatar__wrapper_avatar'

    DAY_INPUT = 'select[name="BirthDay"]'
    DAY_INPUT_CHILD = 'select[name="BirthDay"] option[value="%d"]'
    MONTH_INPUT = 'select[name="BirthMonth"]'
    MONTH_INPUT_CHILD = 'select[name="BirthMonth"] option[value="%d"]'
    YEAR_INPUT = 'select[name="BirthYear"]'
    YEAR_INPUT_CHILD = 'select[name="BirthYear"] option[value="%d"]'

    DAY_VALUE = '.form__row__subwidget_short div.form__select__box'
    MONTH_VALUE = '.form__row__subwidget_large div.form__select__box__text'
    YEAR_VALUE = '.form__row__shift-small.form__row__subwidget_medium div.form__select__box__text'

    IMAGE_INPUT = 'input[name="avatar"]'
    SAVE_IMAGE_BUTTON = 'div[data-fire="save"]'
    CANCEL_IMAGE_BUTTON = 'div[data-fire="cancel"]'
    LOAD_IMAGE_ERROR = 'div.notify'
    LOAD_IMAGE_ERROR_MESSAGE = 'div.notify .js-error.notify-message .js-txt'

    LOGOUT_BUTTON = '#PH_logoutLink'
    LOGOUT_MESSAGE = 'div[class="c012"]'
    HELP_BUTTON = '#settigns_toolbar__right  a.b-toolbar__btn'

    SUBMIT_BUTTON = 'div.form__actions__inner button[type="submit"]'

    OK_AFTER_SUBMIT_URI = 'https://e.mail.ru/settings?result=ok&afterReload=1'
    AFTER_LOGOUT_URI = 'https://mail.ru/?from=logout'
    LOGIN_URI = 'https://e.mail.ru/login\?.*'
    HELP_URI = 'https://help.mail.ru/mail-help/settings/userinfo'

    def set_town(self, town):
        element = wait_for_element_by_selector(self.driver, self.TOWN)
        element.clear()
        element.send_keys(town)

    def save(self):
        element = wait_for_element_by_selector(self.driver, self.SAVE)
        element.click()

    def cancel(self):
        CANCEL_NOT_FULL_SCREEN = '#formPersonal a.btn'
        try:
            self.driver.find_element_by_css_selector(CANCEL_NOT_FULL_SCREEN).click()
        except NoSuchElementException:
            self.driver.find_element_by_css_selector(self.CANCEL).click()

    def get_top_message(self):
        element = wait_for_element_by_selector(self.driver, self.TOP_MESSAGE)
        return element.text

    def get_town_message(self):
        element = wait_for_element_by_selector(self.driver, self.TOWN_ERROR)
        return element.text

    def uncheck_tick(self):
        wait_for_element_by_selector(self.driver, self.TIMEZONE_TICK)
        tick = self.driver.find_element_by_css_selector(self.TIMEZONE_TICK)
        if tick.is_selected():
            tick.click()

    def get_timezone_selector_first_value(self):
        return self.driver.find_element_by_css_selector(self.TIMEZONE_SELECTOR_DIV).text

    def wait_for_timezone_selector_first_value(self, text):
        return wait_for_text_by_selector(self.driver, self.TIMEZONE_SELECTOR_DIV, text)

    def get_url_phone_link(self):
        element = wait_for_element_by_selector(self.driver, self.PHONE_LINK)
        return element.get_attribute("href")  

    def wait_load_image(self, file_name):
        image_path = (os.path.dirname(os.path.abspath(__file__))+file_name).replace("pages", "")
        self.driver.find_element_by_css_selector(self.LOAD_IMAGE).send_keys(image_path)  

    def get_image_error_message(self):
        return wait_for_element_by_selector(self.driver, self.LOAD_IMAGE_ERROR_MESSAGE).text     
    
    def get_save_avatar_button_value(self):
        return wait_for_element_by_selector(self.driver, self.SAVE_AVATAR_TEXT).text
           
    def get_cancel_avatar_button_value(self):
        return wait_for_element_by_selector(self.driver, self.CANCEL_AVATAR_TEXT).text

    def get_save_avatar_button(self):
        return wait_for_element_by_selector(self.driver, self.SAVE_IMAGE_BUTTON)
           
    def get_cancel_avatar_button(self):
        return wait_for_element_by_selector(self.driver, self.CANCEL_AVATAR_TEXT)

    def dismiss_snapshot_request(self):
        make_snapshot = self.driver.find_element_by_css_selector(self.MAKE_SNAPSHOT)
        if make_snapshot.is_enabled():    
            make_snapshot.click()
            self.driver.switch_to_alert()
            Alert(self.driver).dismiss()   

    def set_last_name(self, last_name):
        last_name_elem = wait_for_element_by_selector(self.driver, self.LAST_NAME)
        last_name_elem.clear()
        last_name_elem.send_keys(last_name)        


    def get_last_name(self):
        return wait_for_element_by_selector(self.driver, self.LAST_NAME).get_attribute("value")     
    
    def get_first_name(self):
        return wait_for_element_by_selector(self.driver, self.FIRST_NAME).get_attribute("value")     

    def get_nickname(self):
        return wait_for_element_by_selector(self.driver, self.NICK_NAME).get_attribute("value")    

    def get_last_name_error_message(self):
        return  wait_for_element_by_selector(self.driver, self.LAST_NAME_ERROR).text 

    def clear_town(self):
        wait_for_element_by_selector(self.driver, self.TOWN).clear()

    def get_suggests_for_town(self):
        wait_for_element_by_xpath(self.driver, self.SUGGESTS_ITEM)
        suggests = self.driver.find_elements_by_xpath(self.SUGGESTS_ITEM)
        return [suggest.text for suggest in suggests]

    def get_birth_day(self):
        return wait_for_element_by_selector(self.driver, self.DAY_VALUE).text

    def get_birth_month(self):
        return wait_for_element_by_selector(self.driver, self.MONTH_VALUE).text

    def get_birth_year(self):
        return wait_for_element_by_selector(self.driver, self.YEAR_VALUE).text


    def wait_for_suggests_invisible(self):
        return wait_for_element_by_xpath(self.driver, self.SUGGESTS, False)

    def wait_for_last_suggest(self, text):
        locator = f'{self.SUGGESTS_ITEM}[last()]'
        return wait_for_text_by_xpath(self.driver, locator, text)

    def get_unselected_gender(self):
        gender_male = wait_for_element_by_selector(self.driver, self.GENDER_MALE)
        gender_female = wait_for_element_by_selector(self.driver, self.GENDER_FEMALE)
        return gender_female if gender_male.is_selected() else gender_male    

    def get_image(self):        
        self.config.read('test_data.ini')
        return self.config['DEFAULT']['ImageFile']

    def click_submit_button(self):
        self.click_element(self.SUBMIT_BUTTON, False)

    def input_firstname(self, firstName = 'test1'):
        self.clear_and_send_keys_to_input(self.FIRST_NAME, firstName, False)

    def input_lastname(self, lastName = 'test1'):
        self.clear_and_send_keys_to_input(self.LAST_NAME, lastName, False)

    def input_nickname(self, nickName = 'test1'):
        self.clear_and_send_keys_to_input(self.NICK_NAME, nickName, False)

    def wait_for_ok_after_submit(self):
        wait_redirect(self.driver, self.OK_AFTER_SUBMIT_URI)

    def input_image_and_get_new_image_url(self, name = 'test.png'):
        last_url = self.get_avatar_image_url()
        image_path = (os.path.dirname(os.path.abspath(__file__))+name).replace("pages", "")
        self.clear_and_send_keys_to_input(self.IMAGE_INPUT, image_path, False, False)
        save_image_button = self.get_save_avatar_button()
        save_image_button.click()
        start = time.time()
        while time.time() < start + 30:
            if last_url != self.get_avatar_image_url():
                return self.get_avatar_image_url()
        return last_url



    def get_avatar_image_url(self):
        return wait_for_element_by_selector(self.driver, self.IMAGE_AVATAR).value_of_css_property("background-image")

    def click_save_image_button(self):
        self.click_element(self.SAVE_IMAGE_BUTTON, True)

    def open_settings_in_new_window(self):
        self.driver.execute_script('''window.open("https://e.mail.ru/settings?result=ok&afterReload=1","_blank");''')
        self.switch_to_window(1)

    def click_logout_button(self):
        wait_for_element_by_selector(self.driver, self.LOGOUT_BUTTON)
        self.click_element(self.LOGOUT_BUTTON, False)

    def wait_for_logout_message(self):
        wait_for_element_by_selector(self.driver, self.LOGOUT_MESSAGE, False)

    def wait_for_logout(self):
        wait_redirect(self.driver, self.AFTER_LOGOUT_URI)

    def match_to_login_URI(self):
        wait(self.driver, expected_conditions.url_matches(self.LOGIN_URI))

    def click_on_day_input(self):
        self.click_element(self.DAY_INPUT, False)

    def click_on_day_child_input(self, day_num = 20):
        self.click_element(self.DAY_INPUT_CHILD % day_num, False)

    def click_on_month_input(self):
        self.click_element(self.MONTH_INPUT, False)

    def click_on_month_child_input(self, month_num = 12):
        self.click_element(self.MONTH_INPUT_CHILD % month_num, False)

    def click_on_year_input(self):
        self.click_element(self.YEAR_INPUT, False)

    def click_on_year_child_input(self, year_num = 1997):
        self.click_element(self.YEAR_INPUT_CHILD % year_num, False)

    def click_on_help(self):
        self.click_element(self.HELP_BUTTON, False)

    def wait_for_help(self):
        wait_redirect(self.driver, self.HELP_URI)
