from globals import *
import sys
import log

pnl = log.print_and_log


def userdisable(name):
    click(CheckBox(to_left_of=name))
    click(Button('Disable'))
    loading()
    if Text('Some users cannot be Disabled').exists():
        click(Button('OK'))
    else:
        click(Button('Yes'))
    loading()


def userdelete(name):
    click(CheckBox(to_left_of=name))
    click(Button('Delete'))
    loading()
    try:
        if Button('Confirm').exists():
            click(Button('Confirm'))
        else:
            click(Button('OK'))
        loading()
    except LookupError as e:
        pnl(e)


# Navigates to assigned extensions, checks if a user's extension can be found, and returns true/false
# Implement accordingly!
def usercheck(name):
    exists = None
    while exists is None:
        try:
            nav_assigned()
            loading()
            wait_until(TextField('Search').exists)
            write('', into='Search')
            write(name, into='Search')
            press(ENTER)
            loading()
            if Text('No results').exists():
                exists = False
            else:
                exists = Button(name).exists()
        except LookupError as e:
            pnl(e)
    return exists


def remove(data, count, line):
    remaining_users = count - line
    pnl('{0} extensions remaining to be removed'.format(remaining_users))
    nav_unassigned()
    full_name = data['name']
    email = data['emailAddress']
    pnl('Checking for {0}\'s assigned RingCentral Extension, please wait...'.format(full_name))
    loading()
    write('Ext', into='Search')
    press(ENTER)
    loading()
    click(Button("Ext", below="Name"))
    loading()
    write(data['emailAddress'], into='Email Address')
    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
    else:
        pnl('{0} <{1}> does not have a valid email address. Skipping...'.format(full_name, email))
        ext = "No results found"
        return full_name, ext
    loading()
    if Text('Duplicate Email Association').exists():
        e = grab_table_value("Ext")
        ext = e[0]
        fn = grab_table_value("Name")  # Get the full name as registered in RingCentral
        full_name = fn[0]
        pnl('{0} is assigned extension {1}. Unassigning...'.format(full_name, ext))
        userexists = usercheck(full_name)
        if not userexists:
            try:
                pnl('There was an error removing {0}\'s extension.'.format(full_name))
                confirm = input('Try removing this user manually and enter any key to continue or [e] to exit.')
                if confirm == 'e'.strip('[]') or confirm == 'E'.strip('[]'):
                    kill_browser()
                    sys.exit('Exiting')
                else:
                    pnl('Continuing to the next entry')
            except exceptions.TimeoutException:
                pnl('Waiting for confirmation timed out. Continuing to the next entry')
            finally:
                return
    elif Text('Email address is already in use.').exists():
        loading()
        pnl('Unable to retrieve {0}\'s extension using the email address. Will try to find the extension '
            'based on user\'s display name.'.format(full_name))
        userexists = usercheck(full_name)
        if userexists:
            validateext = False
            ext = Text(to_right_of=Button(full_name), below='Ext').value
            while not validateext:  # Note to future Julio: please fix this. Reading this is giving me anxiety.
                confirm = input(  # Note to past Julio: leave more specific comments next time, dummy. - Future Julio
                    'Press ENTER to confirm that {0} is the correct extension for {1}. If not, input the correct '
                    'extension or [s] to skip this user.'.format(ext, full_name))
                if confirm.strip('[]') == 's' or confirm.strip('[]') == 'S':
                    ext = "Exttension removal cancelled"
                    return full_name, ext
                elif not confirm:
                    validateext = True
                elif not isinstance(confirm, int):
                    pnl('Please input a valid number value')
                else:
                    ext = confirm
            pnl('{0} is assigned extension {1}. Unassigning...'.format(full_name, ext))
        else:
            pnl('{0} not found. Skipping...'.format(full_name))
            ext = "No results found"
            return full_name, ext
    else:
        pnl('{0} does not have an assigned extension.'.format(full_name))
        ext = "No results found"
        return full_name, ext

    deletetry = 0
    while userexists:
        deletetry += 1
        if deletetry >= 6:
            pnl(
                'Maximum attempts for account removal failed. Please manually delete {0}, Ext. {1} from RingCentral.'.format(
                    full_name, ext))
            break
        pnl('Account removal attempt {0} out of 5.'.format(deletetry))
        if deletetry == 5:
            pnl('Final account removal attempt for {0}...'.format(full_name))
        enabled = find_all(S('.rc-icon-user-enabled', to_left_of=Button(full_name)))
        disabled = find_all(S('.rc-icon-user-disabled', to_left_of=Button(full_name)))
        inactive = find_all(S('.rc-icon-not-activated', to_left_of=Button(full_name)))
        if enabled:
            userdisable(full_name)
            del userexists
            userexists = usercheck(full_name)
        elif disabled:
            userdelete(full_name)
            del userexists
            userexists = usercheck(full_name)
        elif inactive:
            userdelete(full_name)
            del userexists
            userexists = usercheck(full_name)
        else:
            del userexists
            userexists = usercheck(full_name)
    return full_name, ext
