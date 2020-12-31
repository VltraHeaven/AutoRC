from helium import *
import csv
import time

# Helium Config
Config.implicit_wait_secs = 15


# Import userlist.csv and save to dictionary

start_chrome('https://login.ringcentral.com/')
click('Single Sign-on')

print('Enter your email address in the browser and click "Submit" to log into RingCentral.')
print('This script will continue when you have successfully accessed the Admin Portal.')
wait_until(Text("Admin Portal").exists, timeout_secs=120, interval_secs=.5)

with open(r'C:\Users\JHawthor\Documents\New Hire Bulk Uploads\UserLists\sd-107817-userlist.csv') as userlist:
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
        write('app', into='Search Users')
        press(ENTER)
        time.sleep(5)
        click('Ext. with RingCentral Phone app')
        write(nhemail, into='Email Address')
        write(nhfirstname, into='First Name')
        write(nhlastname, into='Last Name')
        write(nhtitle, into='Job Title')
        click('Verify Email Uniqueness')
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
        time.sleep(10)
        wait_until(lambda: not Text('Loading...').exists())
        go_to('https://service.ringcentral.com/application/users/users/default')
        wait_until(lambda: not Text('Loading...').exists())
        time.sleep(5)
        write('', into='Search Users')
        write(nhdisplayname, into='Search Users')
        press(ENTER)
        click(Button(nhdisplayname, to_left_of=ext))
        wait_until(lambda: not Text('Loading...').exists())
        click('Call Handling & Forwarding')
        wait_until(lambda: not Text('Loading...').exists())
        select(ComboBox('Ring For'), '15 Rings / 75 Secs')
        click(Text('Save'))
        print(nhdisplayname + ' has been assigned RingCentral Extension: ' + ext)
        del ext
