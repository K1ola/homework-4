from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import string
import random

def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def wait_for_element(driver, selector):
    return WebDriverWait(driver, 30, 0.1).until(
        expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )

def wait(driver, wait_until=None, timeout=15):
    return WebDriverWait(driver, timeout).until(wait_until)

def wait_redirect(driver, url=None):
    if url is None:
        wait(driver, expected_conditions.url_changes(driver.current_url))
    else:
        wait(driver, expected_conditions.url_matches(url))

def wait_for_element_by_selector(driver, selector, visible=True):
    if visible:
        return WebDriverWait(driver, 30, 0.1).until(
            expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, selector))
        )
    else:
        return WebDriverWait(driver, 30, 0.1).until(
            expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, selector))
        )

def wait_for_element_by_xpath(driver, xpath, visible=True):
    if visible:
        return WebDriverWait(driver, 30, 0.1).until(
            expected_conditions.visibility_of_element_located((By.XPATH, xpath))
        )
    else:
        return WebDriverWait(driver, 30, 0.1).until(
            expected_conditions.invisibility_of_element_located((By.XPATH, xpath))
        )  

def wait_for_element_text(driver, selector, text):
    return WebDriverWait(driver, 30, 0.1).until(
            expected_conditions.text_to_be_present_in_element((By.CSS_SELECTOR, selector), text)
        )  

def wait_for_element_text_by_xpath(driver, selector, text):
    return WebDriverWait(driver, 30, 0.1).until(
            expected_conditions.text_to_be_present_in_element((By.XPATH, selector), text)
        )        