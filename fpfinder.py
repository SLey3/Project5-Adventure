# Method to get the filepath of a txt file by only with the prefix



# Imports
import os
import os.path as path

# file Path Reader

def get_file_fp(prefix):
    # It's important to get the current working directory in order to get correct paths
    cwd = os.getcwd()

    # list thru all directories and files, checking only files and only checks the prefixes for files
    # will return the filepath of the matching file
    for item in os.listdir(cwd):
        if path.isfile(path.join(cwd, item)):
            if item.startswith(prefix) and item.endswith(".txt"):
                return path.join(cwd, item)