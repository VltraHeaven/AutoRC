from helium import *
import csv
import os
import sys
from assign import assign, set_forward
from remove import remove
from selenium.webdriver import ChromeOptions
from selenium.common import exceptions
import time
import log
import logging


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
        self.pnl = log.print_and_log
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

    #   Confirms a file exists at the passed argument path
    def filecheck(self):
        if not os.path.isfile(self.filepath):
            self.pnl("The specified file does not exist.")
            sys.exit()

    #   Iterates over and counts each line of the passed csv
    def usercount(self):
        count = 0
        with open(self.filepath) as file:
            count_line = csv.DictReader(file)
            for _ in enumerate(count_line):
                count += 1
        self.pnl('{0} extensions will be processed.'.format(str(count)))
        return count

    #   Iterates over each line of passed csv assigns the value of each column to a variable, creates a new RingCentral
    #   extension and sets the required default extension forwarding settings
    def new_ext(self):
        self.filecheck()
        total = self.usercount()
        result = {}
        with open(self.filepath) as userlist:
            reader = csv.DictReader(userlist)
            for line_num, row in enumerate(reader):
                # row keys: ['givenName'], ['surname'], ['name'], ['emailAddress'], ['Title'], ['Department']
                name, ext = assign(row, total, line_num)
                if name:
                    num = set_forward(name, ext)
                    if name and ext and num:
                        number = '{0}, {1}'.format(num, ext)
                        result[name] = number
                    elif name and num:
                        result[name] = num
                    elif name and ext:
                        result[name] = '{0}, set forwarding configuration manually'.format(ext)
                    else:
                        result[name] = "Extension assignment failed"
                    self.pnl('Extension assignment and configuration for {0} successful.'.format(name))
                else:
                    result[row["name"]] = "Extension assignment failed"
        self.pnl('RingCentral accounts created successfully.')
        entry = 0
        for key, value in result.items():
            entry += 1
            self.pnl('{0}. Name: {1}, Extension: {2}'.format(entry, key, value))
        kill_browser()

    #   Iterates over each line of passed csv assigns the value of each column to a variable and removes the
    #   assigned extension
    def del_ext(self):
        self.filecheck()
        total = self.usercount()
        result = {}
        with open(self.filepath) as userlist:
            reader = csv.DictReader(userlist)
            for line_num, row in enumerate(reader):
                name, ext = remove(row, total, line_num)
                result[name] = ext
                self.pnl('Extension removal for {0} complete.'.format(name))
        self.pnl('RingCentral accounts successfully removed.')
        entry = 0
        for key, value in result.items():
            entry += 1
            self.pnl('{0}. Name: {1}, Extension: {2}'.format(entry, key, value))
        kill_browser()
