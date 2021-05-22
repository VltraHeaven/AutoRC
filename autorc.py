import argparse
import sys
from users import Users
import traceback
import log
import logging


# Entrypoint
def main():
    # CLI Frontend  functionality
    def init_argparse() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            usage="python " + sys.argv[0] + " [-h] [-a | -r] [file]",
            description="description: Automatically assign or remove RingCentral extensions."
        )
        group = parser.add_mutually_exclusive_group()
        group.add_argument('-a', '--assign', help='Assign RingCentral extensions', action='store_true')
        group.add_argument('-r', '--remove', help='Remove RingCentral extension assignments', action='store_true')
        parser.add_argument('file',
                            help='Path to the userlist .csv file.\nThe .csv must at least have the following '
                                 'case-sensitive headers: givenName,surname,name,emailAddress,Title,Department\n')
        return parser

    init_args = init_argparse()
    aparser = init_args.parse_args()

    if aparser.assign:
        if not aparser.file:
            print(aparser.usage)
            print(aparser.description)
        else:
            assign_init = Users(aparser.file)
            assign_init.new_ext()
            logging.shutdown()
            sys.exit(0)
    elif aparser.remove:
        if not aparser.file:
            print(aparser.usage)
            print(aparser.description)
        else:
            remove_init = Users(aparser.file)
            remove_init.del_ext()
            logging.shutdown()
            sys.exit(0)

    else:
        print(aparser.usage + '\n' + aparser.description)


if __name__ == "__main__":
    main()
