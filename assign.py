from globals import *
import sys
import log

pnl = log.print_and_log


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
        pnl('Checking for available extensions')

        # Grabbing total available extensions, stripping text and converting value to integer
        total_ext = int(Text('Total: ').value.strip('Total: '))
        if total_ext > 0:
            pnl('{0} users remaining and {1} available RingCentral extensions'.format(users_sum, total_ext))
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


def assign(data, count, line):
    remaining_users = count - line
    pnl('Assigning {0} a RingCentral Extension, please wait...'.format(data['name']))
    available_ext(remaining_users)
    loading()
    try:
        wait_until(Text("Ext. with RingCentral Phone app").exists)
    except exceptions.TimeoutException:
        time.sleep(3)
    finally:
        click('Ext. with RingCentral Phone app')
    loading()
    write(data['emailAddress'], into='Email Address')
    if not Button('Verify Email Uniqueness').is_enabled():
        pnl('Invalid email address. Skipping...')
        return False, False
    click(Button('Verify Email Uniqueness'))
    loading()
    if Text('Duplicate Email Association').exists():
        ext = grab_table_value("Ext")
        full_name = grab_table_value("Name")
        pnl('{0} has already been assigned extension {1}'.format(full_name[0], ext[0]))
        return full_name[0], ext[0]
    elif Text('Your email address is unique').exists():
        click(Button('OK'))
    else:
        full_name = data['name']
        ext = False
        pnl('An extension for {0} has already been assigned but could not be retrieved.'.format(full_name))
        return full_name, ext
    write(data['givenName'], into='First Name')
    write(data['surname'], into='Last Name')
    write(data['Title'], into='Job Title')
    write(data['Department'], into='Department')
    if not RadioButton('Send Invite').is_selected():
        click(RadioButton('Send Invite'))

    if CheckBox('Yes, I would like to receive information on product education, training materials, etc').is_checked():
        click(CheckBox('Yes, I would like to receive information on product education, training materials, etc'))
    full_name = data['name']
    ext = TextField('Extension Number').value
    loading()
    click(Text('Save'))
    loading()
    pnl('{0} has been assigned RingCentral Extension: {1}'.format(full_name, ext))
    return full_name, ext


def set_forward(name, ext):
    nav_assigned()
    loading()
    num = False
    try:
        select(ComboBox('Show:'), 'All')
    except exceptions.NoSuchElementException:
        try:
            select(ComboBox('Show:'), '500')
        except exceptions.NoSuchElementException:
            pass
    loading()
    write('', into='Search')
    write(name, into='Search')
    press(ENTER)
    loading()
    if not Button(name).exists() and ext:
        write('', into='Search')
        write(ext, into='Search')
        press(ENTER)
        loading()
        if not Button(name).exists():
            pnl("Was unable to set forwarding options for {0}, please set this user's forwarding options manually."
                .format(name))
            return num
    elif not Button(name).exists():
        pnl("Was unable to set forwarding options for {0}, please set this user's forwarding options manually."
            .format(name))
        return num
    while not num:
        try:
            n = grab_table_value("Number")
            num = n[0]
            if num == (False, ""):
                pnl("{0} has not been assigned a direct RingCentral number.".format(name))
                num = input("Please assign this user a direct RingCentral number and enter the value. Format: (000) "
                            "000-0000")
        except exceptions.NoSuchElementException:
            pnl("Unable to capture {0}\'s RingCentral number.".format(name))
            num = input("Please type in the value under the 'Number' column for this user. Format: (000) "
                        "000-0000")
        finally:
            pnl("{0}\'s number is {1}".format(name, num))
    click(Button(name))
    loading()
    rings_set = False
    max_rings = '15 Rings / 75 Secs'
    while not rings_set:
        if not ComboBox("Ring For").exists():
            try:
                wait_until(Text('Call Handling & Forwarding').exists, timeout_secs=120, interval_secs=.5)
                click('Call Handling & Forwarding')
                loading()
            except exceptions.TimeoutException as e:
                pnl(e)
                continue
        try:
            wait_until(ComboBox('Ring For', to_left_of='Desktop').exists, timeout_secs=120, interval_secs=.5)
            current_rings = ComboBox('Ring For').value
        except exceptions.StaleElementReferenceException as e:
            pnl(e)
            continue
        except exceptions.TimeoutException as e:
            pnl(e)
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
    pnl('Forwarding settings for {0} have been set.'.format(name))
    return num
