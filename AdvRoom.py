# File: AdvRoom.py
# Name: Sergio Ley Languren

"""This module is responsible for modeling a single room in Adventure."""

#########################################################################
# Your job in this assignment is to fill in the definitions of the      #
# methods listed in this file, along with any helper methods you need.  #
# The public methods shown in this file are the ones you need for       #
# Milestone #1.  You will need to add other public methods for later    #
# milestones, as described in the handout.                              #
#########################################################################
from typing import Union, List
from textwrap import fill

# Constants

MARKER = "-----"

class AdvRoom:

    visited = False

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._sdesc = shortdesc
        self._ldesc = longdesc
        self._passages = passages

    @property
    def has_been_visited(self) -> bool:
        """
        returns whether the room has been visited or not
        """
        return self.visited

    def get_name(self):
        """Returns the name of this room.."""
        return self._name

    def get_short_description(self):
        """Returns a one-line short description of this room.."""
        return self._sdesc

    def get_long_description(self):
        """Returns the long description describing this room."""
        return self._ldesc

    def get_text(self):
        """
        Gets the text describing the room depending on visited status
        """
        if self.has_been_visited:
            return self.get_short_description()
        return self.get_long_description()

    def get_passages(self):
        """Returns the dictionary mapping directions to names."""
        return self._passages.copy()

    def set_visited(self):
        """
        Sets the rooms visitation status
        """
        self.visited = True

# Method to read a room from a file and helper functions

def _parse_text(txt_obj: List[str]) -> Union[str, str]:
    """
    Seperates text into short and long descriptions
    """
    short_desc = txt_obj.pop(0) # Short description is always first in the list

    long_desc = ""

    print(txt_obj)

    for txt in txt_obj:
        if "." in txt:
            txt = txt.replace(".", ".\n")

            # if the end of the line is not the end of a sentence, a space must be added in order to prevent words unececessarily combining
            if txt[-1] != ".\n":
                txt_split = txt.rsplit(txt[-1], 1) # isolate the last character in the string from the rest of the string
                txt_split[1] = txt_split[1].replace("", f"{txt[-1]} ") # adds the last character with space
                txt = "".join(txt_split) # reform string
           
        else:
            txt = txt.replace(txt[-1], f"{txt[-1]} ")
        long_desc += txt
    
    long_desc = fill(long_desc) # make line indents even
    
    return short_desc, long_desc


def read_adventure(f):
    """Reads adventure rooms from file, returning None at the end."""
    name = f.readline().rstrip()             # Read the room name
    if name == "":                           # Returning None at the end
        return None

    text = [ ]                               # Read the room text
    finished = False
    while not finished:
        line = f.readline().rstrip()
        if line == MARKER:
            finished = True
        else:
            text.append(line)

    answers = { }                            # Read the answer dictionary
    finished = False
    while not finished:
        line = f.readline().rstrip()
        if line == "":
            finished = True
        else:
            colon = line.find(":")
            if colon == -1:
                raise ValueError("Missing colon in " + line)
            response = line[:colon].strip().upper()
            next_room = line[colon + 1:].strip()
            answers[response] = next_room

    short_desc, long_desc = _parse_text(text)

    # print("\n--------------------------")
    # print(f"NAME: {name}")
    # print(f"SHORT DESC: {short_desc}")
    # print(f"LONG DESC: {long_desc}")
    # print(f"ANSWERS: {answers}")
    # print("--------------------------\n")

    return AdvRoom(name, short_desc, long_desc, answers)  # Return the completed object