from globals import *
import sys


def available_ext(users_sum):
    need_ext = True
    while need_ext:
        nav_unassigned()
        wait_until(TextField('Search').exists)
        write('app', into='Search')
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
                    "or [e] to exit".format(users_sum))
                if confirm.strip('[]') == 'e' or confirm.strip('[]') == 'E':
                    kill_browser()
                    sys.exit('Exiting')
            finally:
                time.sleep(1)


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
    write('', into='Search')
    write(ext, into='Search')
    press(ENTER)
    loading()
    try:
        select(ComboBox('Show:'), 'All')
    except exceptions.NoSuchElementException:
        try:
            select(ComboBox('Show:'), '500')
        except exceptions.NoSuchElementException:
            pass
    if not Text(fn).exists() or not Text(ln).exists():
        write('', into='Search')
        write(fn + ' ' + ln, into='Search')
        press(ENTER)
        loading()
        try:
            wait_until(Button(fn, below='Name').exists)
            wait_until(Button(fn, below='Name').is_enabled, timeout_secs=60, interval_secs=.5)
        except exceptions.NoSuchElementException:
            try:
                wait_until(Button(ln, below='Name').exists)
                wait_until(Button(ln, below='Name').is_enabled, timeout_secs=60, interval_secs=.5)
            except exceptions.NoSuchElementException as e:
                print('Forwarding settings for ' + fn + ' ' + ln + ' could not be set')
                print(e)
                return
            else:
                click(Button(ln, below='Name'))
        else:
            click(Button(fn, below="Name"))
    else:
        try:
            wait_until(Button(ln, below='Name').exists)
            wait_until(Button(ln, below='Name').is_enabled, timeout_secs=60, interval_secs=.5)
        except exceptions.NoSuchElementException:
            try:
                wait_until(Button(fn, below='Name').exists)
                wait_until(Button(fn, below='Name').is_enabled, timeout_secs=60, interval_secs=.5)
            except exceptions.NoSuchElementException as e:
                print('Forwarding settings for ' + fn + ' ' + ln + ' could not be set')
                print(e)
                return
            else:
                click(Button(fn, below="Name"))
        else:
            click(Button(ln, below='Name'))
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
