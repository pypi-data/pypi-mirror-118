import sys

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from time import time, ctime, sleep


def init(timer=20):
    wa = {}

    try:
        wa["options"] = Options()
        wa["options"].add_argument("--no-sandbox")
        wa["options"].add_argument("user-data-dir=" + "cookies")

        wa["display"] = Display(visible=0)
        wa["display"].start()

        wa["driver"] = webdriver.Chrome(options=wa["options"])
        wa["driver"].maximize_window()
        wa["driver"].get('https://web.whatsapp.com')
        sleep(timer)
    except Exception as err:
        wa["rc"] = 1
        print(f'Exception occurred in {sys._getframe(2).f_code.co_name} | {err}')

    return wa


def locate_contact(wa, timer=20):
    try:
        wa["driver"].find_element_by_xpath('//*[@title = "{}"]'.format(wa["contact"])).click()
        sleep(timer)
    except Exception as err:
        wa["rc"] = 1
        print(f'Exception occurred in {sys._getframe(2).f_code.co_name} | {err}')

    return wa


def locate_message_box(wa):
    try:
        wa["msg_box"] = wa["driver"].find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[1]')
    except Exception as err:
        wa["rc"] = 1
        print(f'Exception occurred in {sys._getframe(2).f_code.co_name} | {err}')

    return wa


def send_message(wa, timer=15):
    try:
        # Put the message in one-block
        for i in wa["message"]:
            wa["msg_box"].send_keys(i + Keys.SHIFT + Keys.RETURN)

        wa["msg_box"].send_keys(Keys.ENTER)

        sleep(timer)
    except Exception as err:
        wa["rc"] = 1
        print(f'Exception occurred in {sys._getframe(2).f_code.co_name} | {err}')

    return wa


def close(wa):
    try:
        wa["driver"].quit()
        wa["display"].stop()
    except Exception as err:
        wa["rc"] = 1
        print(f'Exception occurred in {sys._getframe(2).f_code.co_name} | {err}')

    return wa
