# File: AdvRoom.py
# Name: your name

"""This module is responsible for modeling a single room in Adventure."""

#########################################################################
# Your job in this assignment is to fill in the definitions of the      #
# methods listed in this file, along with any helper methods you need.  #
# The public methods shown in this file are the ones you need for       #
# Milestone #1.  You will need to add other public methods for later    #
# milestones, as described in the handout.                              #
#########################################################################

# Constants

MARKER = "-----"

class AdvRoom:

    def __init__(self, name, shortdesc, longdesc, passages):
        """Creates a new room with the specified attributes."""
        self._name = name
        self._sdesc = shortdesc
        self._ldesc = longdesc
        self._passages = passages

    def get_name(self):
        """Returns the name of this room.."""
        return self._name

    def get_short_description(self):
        """Returns a one-line short description of this room.."""
        return self._sdesc

    def get_long_description(self):
        """Returns the list of lines describing this room."""
        return self._ldesc

    def get_passages(self):
        """Returns the dictionary mapping directions to names."""
        return self._passages.copy()

# Method to read a room from a file

def read_room(f):
    """Reads the next room from the file, returning None at the end."""
    name = f.readline().rstrip()             # Read the room name
    if name == "":                           # Returning None at the end
        return None

    text = [ ]                               # Read the rrom text
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

    return AdvRoom(name, text, answers)  # Return the completed object