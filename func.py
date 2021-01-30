from helium import *
import time
from selenium.webdriver import ChromeOptions
from selenium.common import exceptions
import sys


def login():
    # WebDriver setting
    options = ChromeOptions()
    options.add_argument('--start-maximized')
    # Helium Config
    Config.implicit_wait_secs = 120
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


def available_ext(users_sum):
    need_ext = True
    while need_ext:
        nav_unassigned()
        wait_until(TextField('Search Users').exists)
        write('app', into='Search Users')
        press(ENTER)
        loading()
        select(ComboBox('Show:'), 'All')
        loading()
        print('Checking for available extensions')
        total_ext = int(Text('Total: ').value.strip('Total: '))
        if total_ext > 0:
            print(str(users_sum) + ' users remaining and ' + str(total_ext) + ' available RingCentral extensions')
            need_ext = False
        else:
            try:
                confirm = input(
                    "There are no available extensions. Please purchase {0} extensions and enter any key to continue "
                    "or [e] to exit").format(users_sum)
                if confirm.strip('[]') == 'e' or confirm.strip('[]') == 'E':
                    kill_browser()
                    sys.exit('Terminating')
            finally:
                time.sleep(1)


def loading():
    loaded = False
    while not loaded:
        if Text("Loading").exists():
            print("Waiting for \'Loading...\' prompt to resolve")
            try:
                wait_until(lambda: not Text("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions as e:
                print(e)
                time.sleep(3)
            else:
                time.sleep(3)
        elif Alert("Loading").exists():
            print("Waiting for \'Loading...\' alert to resolve")
            try:
                wait_until(lambda: not Alert("Loading...").exists(), timeout_secs=10, interval_secs=.5)
            except exceptions as e:
                print(e)
                time.sleep(3)
            else:
                time.sleep(3)
        else:
            # print("Loading the RingCentral Webpage")
            del loaded
            loaded = True
            time.sleep(3)


def delete(firstn, lastn, fulln, email, title):
    nav_unassigned()
    print('Checking for ' + fulln + '\'s assigned RingCentral Extension, please wait...')
    loading()
    write('Ext', into='Search Users')
    press(ENTER)
    loading()
    select(ComboBox('Show:'), 'All')
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
        select(ComboBox('Show:'), 'All')
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


def assign(firstn, lastn, fulln, email, title, count, line):
    remaining_users = count - line
    print('Assigning ' + fulln + ' a RingCentral Extension, please wait...')
    available_ext(remaining_users)
    loading()
    try:
        wait_until(Text("Ext. with RingCentral Phone app").exists)
    except exceptions.TimeoutException:
        time.sleep(3)
    finally:
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
    print('{0} has been assigned RingCentral Extension: {1}'.format(fulln, ext))
    return ext


def set_forward(fn, ln, ext):
    nav_assigned()
    loading()
    write('', into='Search Users')
    write(ext, into='Search Users')
    press(ENTER)
    loading()
    select(ComboBox('Show:'), 'All')
    if not Text(ln).exists():
        try:
            wait_until(Button(fn).exists)
            wait_until(Button(fn).is_enabled, timeout_secs=60, interval_secs=.5)
        except exceptions.TimeoutException as e:
            print(e)
        finally:
            click(Button(fn))
    else:
        try:
            wait_until(Button(ln).exists)
            wait_until(Button(ln).is_enabled, timeout_secs=60, interval_secs=.5)
        except exceptions.TimeoutException as e:
            print(e)
        finally:
            click(Button(fn))
    loading()
    wait_until(Text('Call Handling & Forwarding').exists, timeout_secs=60, interval_secs=.5)
    click('Call Handling & Forwarding')

    max_rings = '15 Rings / 75 Secs'
    rings_set = False
    while not rings_set:
        try:
            wait_until(ComboBox('Ring For', to_left_of='Desktop').exists, timeout_secs=60, interval_secs=.5)
            current_rings = ComboBox('Ring For').value
        except exceptions.StaleElementReferenceException as e:
            print(e)
            continue
        if current_rings != max_rings:
            select(ComboBox('Ring For'), max_rings)
            click(Text('Save'))
            loading()
        elif S('.rc-toggle-off', to_left_of='Always ring for at least 30 seconds').exists():
            click(S('.rc-toggle-input', to_left_of='Always ring for at least 30 seconds'))
            click(Text('Save'))
            loading()
        else:
            rings_set = True
    print('Forwarding settings for {0} {1} have been set.'.format(fn, ln))
    del ext
