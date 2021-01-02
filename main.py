from helium import *
import csv
import time
import argparse
import sys
from selenium.webdriver import ChromeOptions

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
                go_to('https://service.ringcentral.com/application/users/users/unassigned')
                nhfirstname = row['givenName']
                nhlastname = row['surname']
                nhdisplayname = row['name']
                nhemail = row['emailAddress']
                nhtitle = row['Title']
                print('Assigning ' + nhdisplayname + ' a RingCentral Extension, please wait...')
                wait_until(lambda: not Text('Loading...').exists())
                time.sleep(5)
                write('app', into='Search Users')
                press(ENTER)
                wait_until(Text("Ext. with RingCentral Phone app").exists)
                time.sleep(5)
                click('Ext. with RingCentral Phone app')
                write(nhemail, into='Email Address')
                write(nhfirstname, into='First Name')
                write(nhlastname, into='Last Name')
                write(nhtitle, into='Job Title')
                if Button('Verify Email Uniqueness').is_enabled():
                    click(Button('Verify Email Uniqueness'))
                else:
                    print(nhdisplayname + ' <' + nhemail + '>' + ' is not a valid email address. Skipping...')
                    continue

                wait_until(lambda: not Text('Loading...').exists())

                if Text('Duplicate Email Association').exists():
                    print(nhdisplayname + ' already has an assigned RingCentral extension')
                    continue
                else:
                    click(Button('OK'))

                if not RadioButton('Send Invite').is_selected():
                    click(RadioButton('Send Invite'))

                if CheckBox('Yes, I would like to receive information on product education, training materials, etc').is_checked():
                    click(CheckBox('Yes, I would like to receive information on product education, training materials, etc'))

                ext = Text(to_right_of='Phone Number:').value
                time.sleep(5)
                click(Text('Save'))
                time.sleep(5)
                wait_until(lambda: not Text('Loading...').exists())
                go_to('https://service.ringcentral.com/application/users/users/default')
                wait_until(lambda: not Text('Loading...').exists())
                time.sleep(5)
                write('', into='Search Users')
                write(nhdisplayname, into='Search Users')
                press(ENTER)
                wait_until(Button(nhdisplayname, to_left_of=ext).is_enabled, timeout_secs=120, interval_secs=.5)
                time.sleep(5)
                click(Button(nhdisplayname, to_left_of=ext))
                wait_until(lambda: not Text('Loading...').exists())
                click('Call Handling & Forwarding')
                wait_until(lambda: not Text('Loading...').exists())
                select(ComboBox('Ring For'), '15 Rings / 75 Secs')
                click(Text('Save'))
                print(nhdisplayname + ' has been assigned RingCentral Extension: ' + ext)
                del ext
        print('RingCentral accounts created successfully.')
        kill_browser()
        sys.exit(0)