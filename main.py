from helium import *
import csv
import argparse
import sys
from selenium.webdriver import ChromeOptions
from func import assign, set_fward

if __name__ == "__main__":

    # Import userlist.csv and save to dictionary
    def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            usage="Usage: " + sys.argv[0] + " [FILE]...",
            description="Description: Needs path to the user list .csv as an argument. e.g. 'python main.py $home\\Documents\\userlist.csv'\nThe .csv must have the following case-sensitive headers: givenName,surname,name,emailAddress,Title\n"
        )
        parser.add_argument('files')
        return parser


    init_args = init_argparse()
    aparser = init_args.parse_args()

    if not aparser.files:
        print(aparser.usage)
        print(aparser.description)
    else:
        # WebDriver setting
        options = ChromeOptions()
        options.add_argument('--start-maximized')

        # Helium Config
        Config.implicit_wait_secs = 60
        start_chrome('https://login.ringcentral.com/', options=options)
        wait_until(Text("Single Sign-on").exists)
        click('Single Sign-on')

        print('Enter your email address in the browser and click "Submit" to log into RingCentral.')
        print('This script will continue when you have successfully accessed the Admin Portal.')
        wait_until(Text("Admin Portal").exists, timeout_secs=120, interval_secs=.5)

        with open(aparser.files) as userlist:
            reader = csv.DictReader(userlist)
            for row in reader:
                nhfirstname = row['givenName']
                nhlastname = row['surname']
                nhdisplayname = row['name']
                nhemail = row['emailAddress']
                nhtitle = row['Title']
                assignedext = assign(nhfirstname, nhlastname, nhdisplayname, nhemail, nhtitle)
                if assignedext is not None:
                    set_fward(nhdisplayname, assignedext)
                del assignedext
        print('RingCentral accounts created successfully.')
        kill_browser()
        sys.exit(0)
