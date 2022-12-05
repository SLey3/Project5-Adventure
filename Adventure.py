# File: Adventure.py
# Name: your name

"""This file runs the Adventure game."""

# Implementation notes
# --------------------
# The only change you need to make in this file is the definition of
# DATA_FILE_PREFIX, which should be one of the following strings:
#
#    "Tiny"      A four-room Adventure with no objects or synonyms
#    "Small"     A 12-room Adventure that tests all the features
#    "Crowther"  The full 77-room Adventure game

from AdvGame import read_game
import os
import os.path as path

# Constants

DATA_FILE_PREFIX = "Tiny"

# Main program

def _get_file_fp(prefix):
    # It's important to get the current working directory in order to get correct paths
    cwd = os.getcwd()

    # list thru all directories and files, checking only files and only checks the prefixes for files
    # will return the filepath of the matching file
    for item in os.listdir(cwd):
        if path.isfile(path.join(cwd, item)):
            if item.startswith(prefix) and item.endswith(".txt"):
                return path.join(cwd, item)

def adventure():
    fp = _get_file_fp(DATA_FILE_PREFIX)

    print(f"FP: {fp}")
    
    with open(fp) as f:
        return read_game(f)

# Startup code

if __name__ == "__main__":
    adventure().run()
