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
from AdvObject import read_object, AdvObject
from typing import Type, Dict, List, Tuple
import sys

OBJECT_PREFIX = "CrowtherO"
SYNOMYNS_PREFIX = "CrowtherS"

class AdvGame:

    disable_txt = False

    prev_room = None

    inventory = set()

    synomyns = { }

    def __init__(self, rooms: Dict[str, Type[AdvRoom]], objects: Dict[str, Type[AdvObject]]):
        self._rooms = rooms
        self._objects = objects
        self._read_synomyns()

    def _read_synomyns(self):
        fp = get_file_fp(SYNOMYNS_PREFIX)

        marker = "="

        with open(fp) as f:
            for line in f.readlines():
                split_line = line.split(marker)
                self.synomyns[split_line[0]] = split_line[1].strip("\n") # synomyns will act as the identifiers when the dictionary is called later in command parsing


    def _print_objects_in_room_or_not(self, room):
        room_objects = room.get_contents()
        if room_objects: # check if the set is not empty
            for obj in room_objects:
                desc = self._objects[obj].get_description()
                print(f"There is {desc} here.\n")

    def get_rooms(self, name):
        """Returns the AdvRoom object with the specified name."""
        return self._rooms[name]

    def add_objects_to_room(self):
        for room in self._rooms.values():
            for obj_name, obj in self._objects.items():
                obj_loc = obj.get_initial_location()

                if obj_loc == "PLAYER":
                    self.inventory.add(obj_name)
                else:
                    room_name = room.get_name()

                    if obj_loc == room_name:
                        room.add_object(obj_name)


    def split_index_value_or_false(self, i, split_list):
        """
        gets the value of a given index from the given list created by `str.split()`
        if IndexError is raised: return False
        """
        try:
            value = split_list[i]
        except IndexError:
            return False
        return value

    def find_room_in_list(self, direction: str, rooms: List[Tuple[str, str , str]]):
        """
        finds the room in the rooms list based on direction and either returns the room name or None 
        if the room could not be found
        """
        for room in rooms:
            if direction == room[0]: # if direction == room direction
                if room[2]: # if room has a key requirement
                    if room[2] in self.inventory: # if room key is in the users inventory then return the room name
                        return room[1]
                else:
                     return room[1]
        return None # else return None


    def run(self):
        """Plays the adventure game stored in this object."""
        current = "START"

        self.add_objects_to_room()

        while current != "EXIT":
            room = self._rooms[current]
            rooms = room.get_passages()
            
            if not self.disable_txt:
                line = room.get_text()
                print(f"{line}\n")

                self._print_objects_in_room_or_not(room)
            else:
                self.disable_txt = False

            forced = self.find_room_in_list("FORCED", rooms)

            # "if not var" is another way to state "if var is None"
            if not forced:

                response = input("> ").strip().upper()

                split_response = response.split(" ", 1)

                if split_response[0] in self.synomyns:
                    arg = self.split_index_value_or_false(1, split_response)

                    response = self.synomyns[split_response[0]]

                    if arg:
                        response = f"{response} {arg}"

                next_rooms = self.find_room_in_list(response, rooms)

                if not next_rooms:
                    next_rooms = self.find_room_in_list("*", rooms)
                if not next_rooms:
                    if response == "HELP":
                        print("\n".join(HELP_TEXT))

                    elif response == "QUIT":
                        sys.exit(0)
                    elif response == "LOOK":
                        print(f"{room.get_long_description()}\n")
                        self._print_objects_in_room_or_not(room)

                    elif response == "INVENTORY":
                        if self.inventory:
                            print("You are carrying:")
                            for item in self.inventory:
                                print(f"\n {self._objects[item].get_description()}")
                            print("\n")
                        else:
                            print("You are empty-handed.\n")

                    # using split as below are to check for TAKE and DROP commands    
                    elif response.split(" ", 1)[0] == "TAKE":
                        arg = response.split(" ", 1)[1]

                        # validate that the arg is an actual object
                        is_object = self._objects.get(arg, False)

                        if is_object:
                            # validate if object is in the current room
                            in_room = room.contains_object(arg)
                            if in_room:
                                self.inventory.add(arg)
                                room.remove_object(arg) # removes object from the room as it goes into the users inventory
                                print("Taken.\n")
                            else:
                                print(f"No item by the name: {arg.lower()} present.\n")
                        else:
                            print(f"No item by the name: {arg.lower()} exists.\n")
                    elif response.split(" ", 1)[0] == "DROP":
                        arg = response.split(" ", 1)[1]

                        # checks if the arg is in the users inventory
                        in_inventory = arg in self.inventory

                        if in_inventory:
                            self.inventory.remove(arg)
                            room.add_object(arg) # add object from user's inventory to the current room
                            print("Dropped.\n")
                        else:
                            print(f"You are not carrying {arg.lower()}.\n")

                    else:
                        print("I don't understand that response. Perhaps my english isn't that good...\n")
                    room.set_visited()
                else:
                    self.prev_room = current
                    current = next_rooms
                    room.set_visited()
            else:
                self._rooms[self.prev_room].unvisit()
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
