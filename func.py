from helium import *
import time


def assign(firstn, lastn, fulln, email, title):
    go_to('https://service.ringcentral.com/application/users/users/unassigned')
    print('Assigning ' + fulln + ' a RingCentral Extension, please wait...')
    wait_until(lambda: not Text('Loading...').exists())
    time.sleep(5)
    write('app', into='Search Users')
    press(ENTER)
    wait_until(Text("Ext. with RingCentral Phone app").exists)
    time.sleep(5)
    click('Ext. with RingCentral Phone app')
    write(email, into='Email Address')
    write(firstn, into='First Name')
    write(lastn, into='Last Name')
    write(title, into='Job Title')
    if Button('Verify Email Uniqueness').is_enabled():
        click(Button('Verify Email Uniqueness'))
    else:
        print(fulln + ' <' + email + '>' + ' does not have a valid email address. Skipping...')
        return

    wait_until(lambda: not Text('Loading...').exists())

    if Text('Duplicate Email Association').exists():
        print(fulln + ' already has an assigned RingCentral extension')
        time.sleep(3)
        ext = Text(below='Ext.').value
        return ext

    else:
        click(Button('OK'))

    if not RadioButton('Send Invite').is_selected():
        click(RadioButton('Send Invite'))

    if CheckBox(
            'Yes, I would like to receive information on product education, training materials, etc').is_checked():
        click(CheckBox('Yes, I would like to receive information on product education, training materials, etc'))

    ext = TextField('Extension Number').value
    time.sleep(5)
    click(Text('Save'))
    time.sleep(5)
    print(fulln + ' has been assigned RingCentral Extension: ' + str(ext))
    return ext


def set_fward(fulln, ext):
    go_to('https://service.ringcentral.com/application/users/users/default')
    wait_until(lambda: not Text('Loading...').exists())
    time.sleep(5)
    write('', into='Search Users')
    write(ext, into='Search Users')
    press(ENTER)
    wait_until(Button(fulln).is_enabled, timeout_secs=120, interval_secs=.5)
    time.sleep(5)
    click(Button(fulln))
    wait_until(lambda: not Text('Loading...').exists())
    click('Call Handling & Forwarding')
    wait_until(lambda: not Text('Loading...').exists())
    select(ComboBox('Ring For'), '15 Rings / 75 Secs')
    click(Text('Save'))
    print('Forwarding settings for ' + fulln + ' have been set.')
    del ext
