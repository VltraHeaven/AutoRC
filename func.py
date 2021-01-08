from helium import *
import time
from selenium.webdriver import ChromeOptions


def login():
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


def nav_assign():
    url = 'https://service.ringcentral.com/application/users/users/default'
    go_to(url)


def nav_unassign():
    url = 'https://service.ringcentral.com/application/users/users/unassigned'
    go_to(url)


def loading():
    wait_until(lambda: not Text("Loading...").exists())
    wait_until(lambda: not Alert("Loading...").exists())
    time.sleep(3)

def delete(firstn, lastn, fulln, email, title):
    nav_unassign()
    print('Checking for ' + fulln + '\'s assigned RingCentral Extension, please wait...')
    loading()
    write('Ext', into='Search Users')
    press(ENTER)
    loading()
    click(Button(below='Name'))
    loading()
    write(email, into='Email Address')
    write(firstn, into='First Name')
    write(lastn, into='Last Name')
    write(title, into='Job Title')
    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
    else:
        print(fulln + ' <' + email + '>' + ' does not have a valid email address. Skipping...')
        return

    loading()

    if Text('Duplicate Email Association').exists():
        loading()
        regname = Text(below='Name').value
        ext = Text(below='Ext.').value
        print(fulln + ' is assigned extension ' + ext + '. Unassigning...')
    elif Text('Email address is already in use.').exists():
        loading()
        print('Unable to retrieve ' + fulln + '\'s extension. Will try to remove based on user\'s name.')
        regname = fulln
    else:
        print(fulln + ' does not have an assigned extension.')
        return

    def usercheck(extension):
        nav_assign()
        loading()
        write('', into='Search Users')
        write(extension, into='Search Users')
        press(ENTER)
        loading()
        select(ComboBox('Show:'), 'All')
        if Button(regname).exists():
            exists = True
        else:
            exists = False
        return exists

    def userdisable():
        click(CheckBox(to_left_of=regname))
        click(Button('Disable'))
        loading()
        if Text('Some users cannot be Disabled').exists():
            click(Button('OK'))
        else:
            click(Button('Yes'))
        loading()

    def userdelete():
        click(CheckBox(to_left_of=regname))
        click(Button('Delete'))
        loading()
        click('Confirm')
        loading()

    userexists = usercheck(ext)
    deletetry = 0
    while userexists:
        deletetry += 1
        if deletetry >= 6:
            print('Maximum attempts for account removal failed. Please manually delete ' + regname + ', Ext. ' + ext + ' from RingCentral.')
            break
        print('Account removal attempt ' + str(deletetry) + ' out of 5.')
        if deletetry == 5:
            print('Final account removal attempt for ' + regname + '...')
        enabled = find_all(S('.rc-icon-user-enabled', to_left_of=regname))
        disabled = find_all(S('.rc-icon-user-disabled', to_left_of=regname))
        inactive = find_all(S('.rc-icon-not-activated', to_left_of=regname))
        if enabled:
            userdisable()
            del userexists
            userexists = usercheck(ext)
        elif disabled:
            userdelete()
            del userexists
            userexists = usercheck(ext)
        elif inactive:
            userdelete()
            del userexists
            userexists = usercheck(ext)
        else:
            del userexists
            userexists = usercheck(ext)


def assign(firstn, lastn, fulln, email, title):
    nav_unassign()
    print('Assigning ' + fulln + ' a RingCentral Extension, please wait...')
    loading()
    write('app', into='Search Users')
    press(ENTER)
    wait_until(Text("Ext. with RingCentral Phone app").exists)
    time.sleep(5)
    click('Ext. with RingCentral Phone app')
    loading()
    write(email, into='Email Address')
    write(firstn, into='First Name')
    write(lastn, into='Last Name')
    write(title, into='Job Title')
    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
    else:
        print(fulln + ' <' + email + '>' + ' does not have a valid email address. Skipping...')
        return

    loading()

    if Text('Duplicate Email Association').exists():
        print(fulln + ' already has an assigned RingCentral extension')
        time.sleep(3)
        ext = Text(below='Ext.').value
        return ext

    else:
        click(Button('OK'))

    if not RadioButton('Send Invite').is_selected():
        click(RadioButton('Send Invite'))

    if CheckBox('Yes, I would like to receive information on product education, training materials, etc').is_checked():
        click(CheckBox('Yes, I would like to receive information on product education, training materials, etc'))

    ext = TextField('Extension Number').value
    time.sleep(5)
    click(Text('Save'))
    time.sleep(5)
    print(fulln + ' has been assigned RingCentral Extension: ' + str(ext))
    return ext


def set_fward(fulln, ext):
    nav_assign()
    loading()
    write('', into='Search Users')
    write(ext, into='Search Users')
    press(ENTER)
    wait_until(Button(fulln).is_enabled, timeout_secs=120, interval_secs=.5)
    time.sleep(5)
    click(Button(fulln))
    loading()
    click('Call Handling & Forwarding')
    loading()
    select(ComboBox('Ring For'), '15 Rings / 75 Secs')
    click(Text('Save'))
    print('Forwarding settings for ' + fulln + ' have been set.')
    del ext
