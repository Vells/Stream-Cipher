#!/usr/bin/env python3
"""
Author: Vela Dimitrova Mineva
Date: 02/20/2015
"""
import sys
import re
import os


try:
    from cipher import Cipher
except ImportError:
    Cipher = None
    sys.stdout.write("Unable to import Cipher from the cipher module\n")
    sys.exit(0)


def display_usage():
    """
    A function that dislays information about running streamcipher.py
    :return: None
    """
    sys.stdout.write("Usage: python {0} --encrypt | --decrypt FILENAME PASSCODE".format(os.path.basename(__file__)))


def get_arguments():
    """
    A function that parses command line arguments given by the user and returns
    action ('--encrypt' or '--decrypt'), filename and passcode.
    If there are missing or unsupported arguments, when running streamcipher.py,
    a message is displayed and the program is terminated.
    :return: (action, filename, passcode)
              type(action) is a string
              type(filename) is a string
              type(passcode) is an int
    """
    actions = ["--encrypt", "--decrypt"]

    if len(sys.argv) != 4:
        display_usage()
        sys.stdout.write("\n{0} takes 4 arguments ({1} given)!\n".format(os.path.basename(__file__), len(sys.argv) - 1))
        sys.exit(0)
    
    if sys.argv[1] not in actions:
        display_usage()
        sys.stdout.write("{0} error: one of the following arguments is required: {1} FILENAME | "
                         "{2} FILENAME\n".format(os.path.basename(__file__), actions[0], actions[1]))
        sys.exit(0)

    if re.search("[^\d*]", sys.argv[3]):
        display_usage()
        sys.stdout.write("{0} error: PASSCODE has to be an integer")
        sys.exit(0)

    return sys.argv[1], sys.argv[2], int(sys.argv[3])

if __name__ == '__main__':

    action, filename, passcode = get_arguments()
    cipher = Cipher(passcode)
    cipher.perform_action(action, filename)