from helium import *
import csv
import argparse
import sys
from func import delete, assign, set_fward, login


class Users:
    def __init__(self, filepath):
        self.filepath = filepath

    def newext(self):
        login()
        with open(self.filepath) as userlist:
            reader = csv.DictReader(userlist)
            for row in reader:
                nhfirstname = row['givenName']
                nhlastname = row['surname']
                nhdisplayname = row['name']
                nhemail = row['emailAddress']
                nhtitle = row['Title']
                assignedext = assign(nhfirstname, nhlastname, nhdisplayname, nhemail, nhtitle)
                if assignedext is not None:
                    set_fward(nhdisplayname, assignedext)
                    del assignedext
                print('Extension assignment and configuration for ' + nhdisplayname + ' complete.')
        print('RingCentral accounts created successfully.')
        kill_browser()
        sys.exit(0)

    def delext(self):
        login()
        with open(self.filepath) as userlist:
            reader = csv.DictReader(userlist)
            for row in reader:
                nhfirstname = row['givenName']
                nhlastname = row['surname']
                nhdisplayname = row['name']
                nhemail = row['emailAddress']
                nhtitle = row['Title']
                delete(nhfirstname, nhlastname, nhdisplayname, nhemail, nhtitle)
                print('Extension removal for ' + nhdisplayname + ' complete.')
        print('RingCentral accounts successfully removed.')
        kill_browser()
        sys.exit(0)


if __name__ == "__main__":

    def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            usage="Usage: " + sys.argv[0] + " [-h] [-a | -r] [file]",
            description="Description: Automatically assign or remove RingCentral extensions."
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-a', '--assign', help='Assign RingCentral extensions', action='store_true')
        group.add_argument('-r', '--remove', help='Remove RingCentral extension assignments', action='store_true')
        parser.add_argument('file',
                            help='Path to the userlist .csv file.\nThe .csv must at least have the following '
                                 'case-sensitive headers: givenName,surname,name,emailAddress,Title\n"')
        return parser


    init_args = init_argparse()
    aparser = init_args.parse_args()

    if aparser.assign:
        if not aparser.file:
            print(aparser.usage)
            print(aparser.description)
        else:
            assign_init = Users(aparser.file)
            assign_init.newext()
    elif aparser.remove:
        if not aparser.file:
            print(aparser.usage)
            print(aparser.description)
        else:
            remove_init = Users(aparser.file)
            remove_init.delext()
    else:
        print(aparser.usage + '\n' + aparser.description)