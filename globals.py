from helium import *
import time
import datetime
from selenium.common import exceptions
import log
import csv
import pandas as pd
from pathlib import Path

pnl = log.print_and_log


# Navigates directly to the Assigned Extensions web-page
def nav_assigned():
    url = 'https://service.ringcentral.com/application/users/users/default'
    go_to(url)
    loading()
    if Text("Choose User Type").exists():
        click(Button("Cancel"))


# Navigates directly to the Unassigned Extensions web-page
def nav_unassigned():
    url = 'https://service.ringcentral.com/application/users/users/unassigned'
    go_to(url)


# Waits until all prompts containing a "Loading..." string no longer exist on the webpage
def loading():
    time.sleep(1)
    loaded = not Text("Loading...").exists()
    while not loaded:
        try:
            wait_until(lambda: not Text("Loading...").exists(), timeout_secs=10, interval_secs=.1)
        except exceptions.TimeoutException or exceptions.NoSuchElementException:
            pass
        loaded = not Text("Loading...").exists()


def grab_table_value(header):
    table_cells = find_all(S("table > tbody > tr > td > span", below=header))
    cell_values = [cell.web_element.text for cell in table_cells]
    return cell_values


def export_csv(filepath, result_df):
    timestamp = '-autorc-{0}_{1}.'.format(datetime.date.today(), datetime.datetime.now().strftime("%H-%M"))
    split_path = filepath.split('.')
    outfile = ''.join(split_path[:1] + [timestamp] + split_path[1:2])
    output = Path(outfile)
    output.parent.mkdir(exist_ok=True)
    try:
        result_df.to_csv(output)
    except IOError:
        pnl("I/O Error while writing to {0}".format(outfile))
        return IOError
    return outfile
