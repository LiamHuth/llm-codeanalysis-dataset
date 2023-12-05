#
#

import os

def read_file(user_input, base_directory="/safe/directory"):
    full_path = os.path.abspath(os.path.join(base_directory, user_input))

    if os.path.commonpath([full_path, base_directory]) == base_directory:
        with open(full_path, 'r') as file:
            return file.read()
    else:
        raise ValueError("Access denied.")

content = read_file(user_supplied_path)
