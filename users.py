from helium import *
import csv
import os
import sys
from assign import assign, set_forward
from remove import remove
from selenium.webdriver import ChromeOptions
from selenium.common import exceptions
import time


class Users:
    def __init__(self, filepath):
        self.filepath = filepath
        # WebDriver setting
        self.options = ChromeOptions()
        self.options.add_argument('--start-maximized')
        # Helium Config
        self.config = Config
        self.config.implicit_wait_secs = 240
        self.exceptions = exceptions
        start_chrome('https://service.ringcentral.com/', options=self.options)
        try:
            wait_until(Text("Single Sign-on").exists)
            click('Single Sign-on')
        except self.exceptions.TimeoutException or self.exceptions.StaleElementReferenceException or self.exceptions.NoSuchElementException:
            print('Click the Single Sign-on button, enter your email address in the browser and click "Submit" to log '
                  'into RingCentral.')
            time.sleep(2)
        else:
            print('Enter your email address in the browser and click "Submit" to log into RingCentral.')
        finally:
            print('This script will continue when you have successfully accessed the Admin Portal.')
        wait_until(Text("Admin").exists, timeout_secs=120, interval_secs=.5)

    def filecheck(self):
        if not os.path.isfile(self.filepath):
            sys.exit("The specified file does not exist.")

    def usercount(self):
        count = 0
        with open(self.filepath) as file:
            count_line = csv.DictReader(file)
            for _ in enumerate(count_line):
                count += 1
        print(str(count) + ' extensions will be processed.')
        return count

    def new_ext(self):
        self.filecheck()
        total = self.usercount()
        with open(self.filepath) as userlist:
            reader = csv.DictReader(userlist)
            for line_num, row in enumerate(reader):
                firstname = row['givenName']
                lastname = row['surname']
                displayname = row['name']
                email = row['emailAddress']
                title = row['Title']
                assignedext = assign(firstname, lastname, displayname, email, title, total, line_num)
                if assignedext is not None:
                    set_forward(firstname, lastname, assignedext)
                    del assignedext
                print('Extension assignment and configuration for ' + displayname + ' complete.')
        print('RingCentral accounts created successfully.')
        kill_browser()

    def del_ext(self):
        self.filecheck()
        total = self.usercount()
        with open(self.filepath) as userlist:
            reader = csv.DictReader(userlist)
            for line_num, row in enumerate(reader):
                firstname = row['givenName']
                lastname = row['surname']
                displayname = row['name']
                email = row['emailAddress']
                title = row['Title']
                remove(firstname, lastname, displayname, email, title, total, line_num)
                print('Extension removal for ' + displayname + ' complete.')
        print('RingCentral accounts successfully removed.')
        kill_browser()
