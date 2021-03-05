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
    click('Confirm')
    loading()


# Navigates to assigned extensions, checks if a user's extension can be found, and returns true/false
# Implement accordingly!
def usercheck(name):
    nav_assigned()
    loading()
    write('', into='Search')
    write(name, into='Search')
    press(ENTER)
    loading()
    exists = False
    if Text('No results').exists():
        return exists
    else:
        exists = Button(name).exists()
        return exists


def remove(firstn, lastn, fulln, email, title, count, line):
    remaining_users = count - line
    pnl('{0} extensions remaining to be removed'.format(remaining_users))
    nav_unassigned()
    pnl('Checking for {0}\'s assigned RingCentral Extension, please wait...'.format(fulln))
    loading()
    write('Ext', into='Search')
    press(ENTER)
    loading()
    click(Button("Ext", below="Name"))
    loading()
    write(email, into='Email Address')
    write(firstn, into='First Name')
    write(lastn, into='Last Name')
    write(title, into='Job Title')
    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
    else:
        pnl('{0} <{1}> does not have a valid email address. Skipping...'.format(fulln, email))
        return
    loading()
    if Text('Duplicate Email Association').exists():
        e = grab_table_value("Ext")
        ext = e[0]
        fn = grab_table_value("Name")  # Get the full name as registered in RingCentral
        fulln = fn[0]
        pnl('{0} is assigned extension {1}. Unassigning...'.format(fulln, ext))
        userexists = usercheck(fulln)
        if not userexists:
            try:
                pnl('There was an error removing {0}\'s extension.'.format(fulln))
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
            'based on user\'s display name.'.format(fulln))
        userexists = usercheck(fulln)
        if userexists:
            validateext = False
            ext = Text(to_right_of=lastn, below='Ext').value
            while not validateext:  # Note to future Julio: please fix this. Reading this is giving me anxiety.
                confirm = input(  # Note to past Julio: leave more specific comments next time, dummy. - Future Julio
                    'Press ENTER to confirm that {0} is the correct extension for {1}. If not, input the correct '
                    'extension or enter [e] to exit'.format(ext, fulln))
                if confirm.strip('[]') == 'e' or confirm.strip('[]') == 'E':
                    kill_browser()
                    sys.exit('Exiting')
                elif not confirm:
                    validateext = True
                elif not isinstance(confirm, int):
                    pnl('Please input a valid number value')
                else:
                    del ext
                    ext = confirm
            pnl('{0} is assigned extension {1}. Unassigning...'.format(fulln, ext))
        else:
            pnl('{0} not found. Skipping...'.format(fulln))
            return
    else:
        pnl('{0} does not have an assigned extension.'.format(fulln))
        return

    deletetry = 0
    while userexists:
        deletetry += 1
        if deletetry >= 6:
            pnl(
                'Maximum attempts for account removal failed. Please manually delete {0}, Ext. {1} from RingCentral.'.format(fulln, ext))
            break
        pnl('Account removal attempt {0} out of 5.'.format(deletetry))
        if deletetry == 5:
            pnl('Final account removal attempt for {0}...'.format(fulln))
        enabled = find_all(S('.rc-icon-user-enabled', to_left_of=Button(fulln)))
        disabled = find_all(S('.rc-icon-user-disabled', to_left_of=Button(fulln)))
        inactive = find_all(S('.rc-icon-not-activated', to_left_of=Button(fulln)))
        if enabled:
            userdisable(fulln)
            del userexists
            userexists = usercheck(fulln)
        elif disabled:
            userdelete(fulln)
            del userexists
            userexists = usercheck(fulln)
        elif inactive:
            userdelete(fulln)
            del userexists
            userexists = usercheck(fulln)
        else:
            del userexists
            userexists = usercheck(fulln)
