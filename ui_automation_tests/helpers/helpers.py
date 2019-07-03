import allure
import datetime
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import date
import logging

d = date.fromordinal(730920)
now = d.strftime("%d-%m-%Y")
path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
screen_dir = os.path.join(path, "screenshot", str(now))


def screen_path():
    global screen_dir
    if not os.path.exists(screen_dir):
        os.makedirs(screen_dir)
        os.chmod(screen_dir, 0o755)
    return screen_dir


def remove_special_characters(text):
    # text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.translate(str.maketrans('', '', '\ / : * ? " < > |'))
    return text

def save_screenshot(driver, name):
    logging.info("name: " + name)
    _name = remove_special_characters(name)
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


def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]


def get_formatted_date_time_h_m_pm_d_m_y():
    time = datetime.datetime.now().strftime("%I:%M%p %d %B %Y").replace("PM", "pm").replace(
        "AM", "am")
    if time[0] == "0":
        time = time[1:]
    return time

def get_unformatted_date_time():
    return datetime.datetime.now()


def get_formatted_date_time_m_d_h_s():
    return datetime.datetime.now().strftime("%m%d%H%M%S")
