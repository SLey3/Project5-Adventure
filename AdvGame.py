# File: AdvGame.py
# Name: your name

"""
This module defines the AdvGame class, which records the information
necessary to play a game.
"""

###########################################################################
# Your job in this assignment is to fill in the definitions of the        #
# methods listed in this file, along with any helper methods you need.    #
# Unless you are implementing extensions, you won't need to add new       #
# public methods (i.e., methods called from other modules), but the       #
# amount of code you need to add is large enough that decomposing it      #
# into helper methods will be essential.                                  #
###########################################################################

from AdvRoom import read_adventure

class AdvGame:

    def __init__(self, prefix):
        """Reads the game data from files with the specified prefix."""
        self._prefix = prefix
        self._room = {}

    def get_room(self, name):
        """Returns the AdvRoom object with the specified name."""
        return self._room[name]

    def run(self):
        """Plays the adventure game stored in this object."""
        current = "START"
        while current != "EXIT":
            room = self._room[current]
            for line in room.get_text():
                print(line)
            forced = answers.get("FORCED", None)

            # "if not var" is another way to state "if var is None"
            if not forced:
                response = input("> ").strip().upper()
                answers = room.get_answers()
                next_room = answers.get(response, None)

                if not next_room:
                    next_room = answers.get("*", None)
                if not next_room:
                    print("I don't understand that response. Perhaps my english isn't that good...")
                else:
                    current = next_room
            else:
                current = forced


def read_game(f):
    """Reads the entire Game from the data file f."""
    rooms = { }
    finished = False
    while not finished:
        room = read_adventure(f)
        if room is None:
            finished = True
        else:
            name = room.get_name()
            if len(rooms) == 0:
                rooms["START"] = room
            rooms[name] = room
    return AdvGame(rooms)

# Constants

HELP_TEXT = [
    "Welcome to Adventure!",
    "Somewhere nearby is Colossal Cave, where others have found fortunes in",
    "treasure and gold, though it is rumored that some who enter are never",
    "seen again.  Magic is said to work in the cave.  I will be your eyes",
    "and hands.  Direct me with natural English commands; I don't understand",
    "all of the English language, but I do a pretty good job.",
    "",
    "It's important to remember that cave passages turn a lot, and that",
    "leaving a room to the north does not guarantee entering the next from",
    "the south, although it often works out that way.  You'd best make",
    "yourself a map as you go along.",
    "",
    "Much of my vocabulary describes places and is used to move you there.",
    "To move, try words like IN, OUT, EAST, WEST, NORTH, SOUTH, UP, or DOWN.",
    "I also know about a number of objects hidden within the cave which you",
    "can TAKE or DROP.  To see what objects you're carrying, say INVENTORY.",
    "To reprint the detailed description of where you are, say LOOK.  If you",
    "want to end your adventure, say QUIT."
]
