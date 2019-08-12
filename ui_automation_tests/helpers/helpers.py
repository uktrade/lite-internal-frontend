import re

import allure
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
import logging

d = date.fromordinal(730920)
now = d.strftime("%d-%m-%Y")
path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
screen_dir = os.path.join(path, "screenshot", str(now))

def get_current_date_time_string():
    return datetime.now().strftime("%Y/%m/%d %H:%M:%S:%f")


def screen_path():
    global screen_dir
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir)
        os.chmod(screen_dir, 0o644)
    return screen_dir


def remove_special_characters(text):
    # text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', '\ / : * ? " < > |'))
    return text


def save_screenshot(driver, name):
    logging.info("name: " + name)
    print("name: " + name)
    _name = remove_special_characters(name)
    print("name: " + _name)
    print("name: " + _name + '-' + now + ".png")

    driver.get_screenshot_as_file(os.path.join(screen_path(), _name + '-' + now + ".png"))
    allure.attach(_name + "-" + now, driver.get_screenshot_as_png(), allure.attachment_type.PNG)


def find_element(driver, by_type, locator):
    delay = 3  # seconds
    try:
        return WebDriverWait(driver, delay).until(EC.presence_of_element_located((by_type, locator)))

    except TimeoutException:
        print("element {} was not found".format(locator))


def is_element_present(driver, how, what):
    """
    Helper method to confirm the presence of an element on page
    :params how: By locator type
    :params what: locator value
    """
    try:
        driver.find_element(by=how, value=what)
    except NoSuchElementException:
        return False
    return True


def click(driver, by_type, locator):
    el = find_element(driver, by_type, locator)
    el.click()


def type_text(driver, text, by_type, locator):
    el = find_element(driver, by_type, locator)
    el.click()
    el.send_keys(text)


def get_text(driver, by_type, locator):
    el = find_element(driver, by_type, locator)
    return el.text


def get_formatted_date_time_h_m_pm_d_m_y():
    time = datetime.now().strftime("%I:%M%p %d %B %Y").replace("PM", "pm").replace(
        "AM", "am")
    if time[0] == "0":
        time = time[1:]
    return time


def get_unformatted_date_time():
    return datetime.now()


def get_formatted_date_time_m_d_h_s():
    return datetime.now().strftime("%m%d%H%M%S")


def get_formatted_date_time_d_h_m_s():
    return datetime.now().strftime(" %d%H%M%S")


def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",
                              element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.7)
    apply_style(original_style)


def get_element_by_text(elements, text: str):
    """
    Loops through the list of elements, checks if the text is equal to
    text and returns the element if so
    """
    for element in elements:
        if element == text:
            return element


def get_element_index_by_text(elements, text: str):
    """
    Loops through the list of elements, checks if the text is equal to
    text and returns the index of it if so
    """
    no = 0
    element_number = -1
    while no < len(elements):
        if elements[no].text == text:
            element_number = no
            break
        no += 1

    return element_number


def get_element_index_by_partial_text(elements, text: str):
    """
    Loops through the list of elements, checks if the text is equal to
    text and returns the index of it if so
    """
    no = 0
    element_number = -1
    while no < len(elements):
        if text in elements[no].text:
            element_number = no
            break
        no += 1

    return element_number


def wait_until_page_is_loaded(driver):
    time_no = 0
    while time_no < 60:
        if driver.execute_script("return document.readyState") == "complete":
            break
        time.sleep(1)
        time_no += 1


def wait_until_menu_is_visible(driver):
    while True:
        try:
            if driver.find_element_by_css_selector('.lite-menu--visible').is_displayed():
                break
        except Exception:
            continue


def select_visible_text_from_dropdown(element, text):
    select = Select(element)
    select.select_by_visible_text(text)


def search_for_correct_date_regex_in_element(element):
    return re.search("([0-9]{1,2}):([0-9]{2})(am|pm) ([0-9][0-9]) (January|February|March|April|May|June|July|August|September|October|November|December) ([0-9]{4,})", element)
