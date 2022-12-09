# File: Adventure.py
# Name: Sergio Ley Languren

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
from fpfinder import get_file_fp

# Constants

DATA_FILE_PREFIX = "CrowtherR"

def adventure():
    fp = get_file_fp(DATA_FILE_PREFIX)
    
    with open(fp) as f:
        return read_game(f)

# Startup code

if __name__ == "__main__":
    adventure().run()
