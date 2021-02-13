from helium import *
import time
from selenium.common import exceptions


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
                time.sleep(2)
            else:
                time.sleep(2)
        elif Alert("Loading").exists():
            print("Waiting for \'Loading...\' alert to resolve")
            try:
                wait_until(lambda: not Alert("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions.TimeoutException or exceptions.NoSuchElementException as e:
                print(e)
                time.sleep(2)
            else:
                time.sleep(2)
        else:
            # print("Loading the RingCentral Webpage")
            del loaded
            loaded = True
            time.sleep(2)

