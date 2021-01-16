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


def nav_assigned():
    url = 'https://service.ringcentral.com/application/users/users/default'
    go_to(url)
    select(ComboBox('Show:'), 'All')


def nav_unassigned():
    url = 'https://service.ringcentral.com/application/users/users/unassigned'
    go_to(url)
    select(ComboBox('Show:'), 'All')


def loading():
    loaddone = False
    while not loaddone:
        if Text("Loading").exists():
            print("Waiting for \'Loading...\' prompt to resolve")
            wait_until(lambda: not Text("Loading...").exists(), timeout_secs=60, interval_secs=.1)
        elif Alert("Loading").exists():
            print("Waiting for \'Loading...\' alert to resolve")
            wait_until(lambda: not Alert("Loading...").exists(), timeout_secs=60, interval_secs=.1)
        else:
            print("Loading the RingCentral Webpage")
            loaddone = True
    countdown = 3
    print("Resuming in " + str(countdown) + " seconds.")
    while countdown > 0:
        time.sleep(1)
        countdown += -1


def delete(firstn, lastn, fulln, email, title):
    nav_unassigned()
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

    def usercheck(query):
        nav_assigned()
        loading()
        write('', into='Search Users')
        write(query, into='Search Users')
        press(ENTER)
        loading()
        exists = Button(regname).exists()
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

    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
    else:
        print(fulln + ' <' + email + '>' + ' does not have a valid email address. Skipping...')
        return

    loading()

    if Text('Duplicate Email Association').exists():
        loading()
        regname = Text(below='Name').value
        ext = Text(below='Ext.', to_right_of=regname).value
        print(fulln + ' is assigned extension ' + ext + '. Unassigning...')
        userexists = usercheck(ext)
    elif Text('Email address is already in use.').exists():
        loading()
        print(
            'Unable to retrieve ' + fulln + '\'s extension using email address. Will try to find the extension based on user\'s display name.')
        regname = fulln
        userexists = usercheck(regname)
        if userexists:
            ext = Text(to_right_of=lastn, below='Number').value
            print(fulln + ' is assigned extension ' + ext + '. Unassigning...')
        else:
            print(fulln + ' not found. Skipping...')
            return
    else:
        print(fulln + ' does not have an assigned extension.')
        return

    deletetry = 0
    while userexists:
        deletetry += 1
        if deletetry >= 6:
            print(
                'Maximum attempts for account removal failed. Please manually delete ' + regname + ', Ext. ' + ext + ' from RingCentral.')
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
    nav_unassigned()
    print('Assigning ' + fulln + ' a RingCentral Extension, please wait...')
    loading()
    wait_until(TextField('Search Users').exists)
    write('app', into='Search Users')
    press(ENTER)
    loading()
    wait_until(Text("Ext. with RingCentral Phone app").exists)
    loading()
    click('Ext. with RingCentral Phone app')
    loading()
    write(email, into='Email Address')
    write(firstn, into='First Name')
    write(lastn, into='Last Name')
    write(title, into='Job Title')
    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
        loading()
    else:
        print(fulln + ' <' + email + '>' + ' does not have a valid email address. Skipping...')
        return

    if Text('Duplicate Email Association').exists():
        ext = Text(below='Ext', to_left_of=email).value
        print(fulln + ' has already been assigned extension ' + ext)
        return ext

    else:
        click(Button('OK'))

    if not RadioButton('Send Invite').is_selected():
        click(RadioButton('Send Invite'))

    if CheckBox('Yes, I would like to receive information on product education, training materials, etc').is_checked():
        click(CheckBox('Yes, I would like to receive information on product education, training materials, etc'))

    ext = TextField('Extension Number').value
    loading()
    click(Text('Save'))
    loading()
    print(fulln + ' has been assigned RingCentral Extension: ' + str(ext))
    return ext


def set_fward(fulln, ext):
    nav_assigned()
    loading()
    write('', into='Search Users')
    write(ext, into='Search Users')
    press(ENTER)
    wait_until(Button(fulln).exists)
    wait_until(Button(fulln).is_enabled, timeout_secs=120, interval_secs=.5)
    loading()
    click(Button(fulln))
    loading()
    click('Call Handling & Forwarding')
    loading()
    select(ComboBox('Ring For'), '15 Rings / 75 Secs')
    loading()
    click(Text('Save'))
    print('Forwarding settings for ' + fulln + ' have been set.')
    del ext
