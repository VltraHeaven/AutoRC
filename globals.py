from helium import *
import time
from selenium.webdriver import ChromeOptions
from selenium.common import exceptions


def login():
    # WebDriver setting
    options = ChromeOptions()
    options.add_argument('--start-maximized')
    # Helium Config
    Config.implicit_wait_secs = 240
    start_chrome('https://service.ringcentral.com/', options=options)
    try:
        wait_until(Text("Single Sign-on").exists)
        click('Single Sign-on')
    except exceptions.TimeoutException or exceptions.StaleElementReferenceException or exceptions.NoSuchElementException:
        print('Click the Single Sign-on button, enter your email address in the browser and click "Submit" to log '
              'into RingCentral.')
        time.sleep(2)
    else:
        print('Enter your email address in the browser and click "Submit" to log into RingCentral.')
    finally:
        print('This script will continue when you have successfully accessed the Admin Portal.')
    wait_until(Text("Admin").exists, timeout_secs=120, interval_secs=.5)


def nav_assigned():
    url = 'https://service.ringcentral.com/application/users/users/default'
    go_to(url)


def nav_unassigned():
    url = 'https://service.ringcentral.com/application/users/users/unassigned'
    go_to(url)


def loading():
    loaded = False
    while not loaded:
        if Text("Loading").exists():
            print("Waiting for \'Loading...\' prompt to resolve")
            try:
                wait_until(lambda: not Text("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions.TimeoutException or exceptions.NoSuchElementException as e:
                print(e)
                time.sleep(3)
            else:
                time.sleep(3)
        elif Alert("Loading").exists():
            print("Waiting for \'Loading...\' alert to resolve")
            try:
                wait_until(lambda: not Alert("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions.TimeoutException or exceptions.NoSuchElementException as e:
                print(e)
                time.sleep(3)
            else:
                time.sleep(3)
        else:
            # print("Loading the RingCentral Webpage")
            del loaded
            loaded = True
            time.sleep(3)

