#!/usr/bin/env python
import sys
import re




if __name__ == "__main__":
    replacement = "----$$$$___"
    target_file = sys.argv[1]
    num_spaces = 2
    with open(target_file, 'r+') as target_file:
        file_content = target_file.read()
        # Get everything down to a single space
        file_content = re.sub(r"[ \t]+", " ", file_content)
        # TODO: Check to make sure the replacement string doesn't already exist in the file somehow
        # Put the replacement characters in there
        file_content = file_content.replace(" ", replacement)
        while replacement in file_content:
            file_content = file_content.replace(replacement, " " * num_spaces, 1)
            num_spaces += 1
        target_file.seek(0)
        target_file.write(file_content)