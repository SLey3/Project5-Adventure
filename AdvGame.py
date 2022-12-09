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

from AdvRoom import read_adventure, AdvRoom
from fpfinder import get_file_fp
from tokenscanner import TokenScanner
from AdvObject import read_object, AdvObject
from typing import Type, Dict
import sys

TokenScanner()


OBJECT_PREFIX = "CrowtherO"

class AdvGame:

    disable_txt = False

    inventory = set()

    token_scanner = TokenScanner()

    def __init__(self, rooms: Dict[str, Type[AdvRoom]], objects: Dict[str, Type[AdvObject]]):
        self._rooms = rooms
        self._objects = objects

    def get_rooms(self, name):
        """Returns the AdvRoom object with the specified name."""
        return self._rooms[name]

    def add_objects_to_room(self):
        for _, room in self._rooms.items():
            for obj_name, obj in self._objects.items():
                obj_loc = obj.get_initial_location()

                if obj_loc == "PLAYER":
                    self.inventory.add(obj_name)

                room_name = room.get_name()

                if obj_loc == room_name:
                    room.add_object(obj_name)


    def run(self):
        """Plays the adventure game stored in this object."""
        current = "START"

        self.add_objects_to_room()

        while current != "EXIT":
            room = self._rooms[current]
            
            if not self.disable_txt:
                line = room.get_text()
                print(f"{line}\n")

                room_objects = room.get_contents()
                if room_objects: # check if the set is not empty
                    for obj in room_objects:
                        desc = self._objects[obj].get_description()
                        print(f"There is {desc} here.\n")
            else:
                self.disable_txt = False

            response = input("> ").strip().upper()
            rooms = room.get_passages()

            forced = rooms.get("FORCED", None)

            # "if not var" is another way to state "if var is None"
            if not forced:
                next_rooms = rooms.get(response, None)

                if not next_rooms:
                    next_rooms = rooms.get("*", None)
                if not next_rooms:
                    if response == "HELP":
                        print("\n".join(HELP_TEXT))
                        self.disable_txt = True
                    elif response == "QUIT":
                        sys.exit(0)
                    elif response == "LOOK":
                        print(room.get_long_description())
                        self.disable_txt = True
                    elif response == "INVENTORY":
                        if self.inventory:
                            print("You are carrying:")
                            for item in self.inventory:
                                print(f"\n {self._objects[item].get_description()}")
                        else:
                            print("You are empty-handed.")
                        self.disable_txt = True
                    else:
                        print("I don't understand that response. Perhaps my english isn't that good...")
                else:
                    room.set_visited()
                    current = next_rooms
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

    objects = { }
    finished = False
    obj_fp = get_file_fp(OBJECT_PREFIX)
    with open(obj_fp) as f:
        while not finished:
            object = read_object(f)
            if object is None:
                finished = True
            else:
                name = object.get_name()
                objects[name] = object

    return AdvGame(rooms, objects)

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
    "want to end your adventure, say QUIT.\n"
]
