# File: AdvObject.py
# Name: Sergio Ley Languren

"""This module defines a class that models an object in Adventure."""

#########################################################################
# Your job in this assignment is to fill in the definitions of the      #
# methods listed in this file, along with any helper methods you need.  #
# You won't need to work with this file until Milestone #4.  In my      #
# solution, none of the milestones required any public methods beyond   #
# the ones defined in this starter file.                                #
#########################################################################

class AdvObject:

    def __init__(self, name, description, location):
        """Creates an AdvObject from the specified properties."""
        self.name = name
        self.description = description
        self.location = location

    def get_name(self):
        """Returns the name of this object."""
        return self.name

    def get_description(self):
        """Returns the description of this object."""
        return self.description

    def get_initial_location(self):
        """Returns the initial location of this object."""
        return self.location

# Method to read an object from a file

def read_object(f) -> AdvObject:
    """Reads the next object from the file, returning None at the end."""
    name = f.readline().rstrip()

    if name == "":
        return None

    finished = False
    text = [] # Below, when text file is parsed, the text list when __getitem__  is called thru the indexes of: 0, 1, 
              # the results should be as follows:
              # text[0] = description
              # text[1] = location

    while not finished:
        line = f.readline().rstrip()
        if line == "":
            finished = True
        else:
            text.append(line)
    return AdvObject(name, text[0], text[1])