from helium import *
import time
from selenium.common import exceptions
import log
import logging

pnl = log.print_and_log

# Navigates directly to the Assigned Extensions web-page
def nav_assigned():
    url = 'https://service.ringcentral.com/application/users/users/default'
    go_to(url)

# Navigates directly to the Unassigned Extensions web-page
def nav_unassigned():
    url = 'https://service.ringcentral.com/application/users/users/unassigned'
    go_to(url)

# Waits until all prompts containing a "Loading..." string no longer exist on the webpage
def loading():
    loaded = False
    while not loaded:
        if Text("Loading").exists():
            pnl("Waiting for \'Loading...\' prompt to resolve")
            try:
                wait_until(lambda: not Text("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions.TimeoutException or exceptions.NoSuchElementException as e:
                pnl(e)
                time.sleep(2)
            else:
                time.sleep(2)
        elif Alert("Loading").exists():
            pnl("Waiting for \'Loading...\' alert to resolve")
            try:
                wait_until(lambda: not Alert("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions.TimeoutException or exceptions.NoSuchElementException as e:
                pnl(e)
                time.sleep(2)
            else:
                time.sleep(2)
        else:
            # pnl("Loading the RingCentral Webpage")
            del loaded
            loaded = True
            time.sleep(2)

