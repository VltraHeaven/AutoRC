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
    if Button(name, below='Name').exists():
        del exists
        exists = True
    return exists


def remove(firstn, lastn, fulln, email, title, count, line):
    remaining_users = count - line
    pnl(str(remaining_users) + ' extensions remaining to be removed')
    nav_unassigned()
    pnl('Checking for ' + fulln + '\'s assigned RingCentral Extension, please wait...')
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
        pnl(fulln + ' <' + email + '>' + ' does not have a valid email address. Skipping...')
        return
    loading()
    if Text('Duplicate Email Association').exists():
        ext = Text(below='Ext', to_left_of=email).value
        regname = Text(below='Name', to_left_of=ext).value  # Get the full name as registered in RingCentral
        pnl(regname + ' is assigned extension ' + ext + '. Unassigning...')
        userexists = usercheck(regname)
        if not userexists:
            try:
                pnl('There was an error removing ' + regname + '\'s extension.')
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
        pnl('Unable to retrieve ' + fulln + '\'s extension using the email address. Will try to find the extension '
                                              'based on user\'s display name.')
        regname = fulln
        userexists = usercheck(regname)
        if userexists:
            validateext = False
            ext = Text(to_right_of=lastn, below='Ext').value
            while not validateext:  # Note to future Julio: please fix this. Reading this is giving me anxiety.
                confirm = input(    # Note to past Julio: leave more specific comments next time, dummy. - Future Julio
                    'Press ENTER to confirm that ' + ext + ' is the correct extension for ' + regname +
                    '. If not, input the correct extension or enter [e] to exit')
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
            pnl(fulln + ' is assigned extension ' + ext + '. Unassigning...')
        else:
            pnl(fulln + ' not found. Skipping...')
            return
    else:
        pnl(fulln + ' does not have an assigned extension.')
        return

    deletetry = 0
    while userexists:
        deletetry += 1
        if deletetry >= 6:
            pnl(
                'Maximum attempts for account removal failed. Please manually delete ' + regname + ', Ext. ' + ext + ' from RingCentral.')
            break
        pnl('Account removal attempt ' + str(deletetry) + ' out of 5.')
        if deletetry == 5:
            pnl('Final account removal attempt for ' + regname + '...')
        enabled = find_all(S('.rc-icon-user-enabled', to_left_of=regname))
        disabled = find_all(S('.rc-icon-user-disabled', to_left_of=regname))
        inactive = find_all(S('.rc-icon-not-activated', to_left_of=regname))
        if enabled:
            userdisable(regname)
            del userexists
            userexists = usercheck(regname)
        elif disabled:
            userdelete(regname)
            del userexists
            userexists = usercheck(regname)
        elif inactive:
            userdelete(regname)
            del userexists
            userexists = usercheck(regname)
        else:
            del userexists
            userexists = usercheck(regname)
