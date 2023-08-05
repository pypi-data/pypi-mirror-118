from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from time import time, ctime, sleep


def init(debug=0, sleep=20):
    # Initialize WhatsApp
    rc = 0
    t = time()

    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("user-data-dir=" + "cookies")
        
        # default debug is set to FALSE
        if debug:
            display = Display(visible=0)
            display.start()

        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        driver.get('https://web.whatsapp.com')

        sleep(sleep)
    except Exception as err:
        print(f'{ctime(t)} | Exception occurred in wa_init() function \n {err}')
        rc = 1

    return rc, driver, display


def close(debug=0, driver, display):
    # close connection to WhatsApp
    driver.quit()

    if debug:
        display.stop()


def locate(sleep=10, river, wa_contact):
    # Find the WhatsApp contact
    rc = 0
    t = time()

    try:
        driver.find_element_by_xpath('//*[@title = "{}"]'.format(wa_contact)).click()
        sleep(sleep)
    except Exception as err:
        print(f'{ctime(t)} | Exception occurred in wa_contact() function \n {err}')
        rc = 1

    return rc


def message(sleep=15, driver, display, wa_message_list):
    rc = 0
    t = time()

    try:
        wa_msg = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[1]')

        # message in one-block
        for i in wa_message_list:
            wa_msg.send_keys(i + Keys.SHIFT + Keys.RETURN)

        wa_msg.send_keys(Keys.ENTER)
        sleep(sleep)

        print(f'{ctime(t)} | WhatsApp message successfully sent!')

        wa_close(driver, display)

    except Exception as err:
        print(f'{ctime(t)} | Exception occurred in wa_contact() function \n {err}')
        rc = 1

    return rc
