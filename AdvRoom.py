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

    forced = False

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._sdesc = shortdesc
        self._ldesc = longdesc
        self._passages = passages
        self._objects = set()

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
        if self.has_been_visited and not self.forced:
            return self.get_short_description()
        return self.get_long_description()

    def get_passages(self):
        """Returns the list containing a tuple with the follow order items: direction, name, key required."""
        return self._passages.copy()

    def set_visited(self):
        """
        Sets the rooms visitation status
        """
        self.visited = True
    
    def unvisit(self):
        """
        Sets the room visitation status to False
        """
        self.visited = False

    def add_object(self, obj_name):
        """
        add object to the room
        """
        self._objects.add(obj_name)

    def remove_object(self, obj_name):
        """
        removes object from the room
        """
        try:
            self._objects.remove(obj_name)
        except KeyError:
            pass
    
    def contains_object(self, name):
        """
        Checks whether an object is in the room
        """
        return name in self._objects
    
    def get_contents(self):
        """
        copy objects set
        """
        return self._objects.copy()


# Method to read a room from a file

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

    passages = []                           # Read the answer dictionary
    finished = False
    key_required = None
    passage = None

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
           
            if "/" in next_room:
                next_room = next_room.split("/")
                passage = next_room[0]
                key_required = next_room[1]
                passages.append((response, passage, key_required))
            else:
                passages.append((response, next_room, key_required))
            key_required = None

    short_desc = text.pop(0)
    long_desc = "\n".join(text)

    return AdvRoom(name, short_desc, long_desc, passages)  # Return the completed object