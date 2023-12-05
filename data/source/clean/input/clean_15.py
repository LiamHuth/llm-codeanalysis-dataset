#
#

import os

ALLOWED_EXTENSIONS = {".txt", ".pdf", ".jpg"}

def read_file(user_input, base_directory="/safe/directory"):
    _, file_extension = os.path.splitext(user_input)

    if file_extension in ALLOWED_EXTENSIONS:
        full_path = os.path.join(base_directory, user_input)

        if os.path.commonprefix([full_path, base_directory]) == base_directory:
            with open(full_path, 'r') as file:
                return file.read()
        else:
            raise ValueError("Access denied.")
    else:
        raise ValueError("Invalid file type.")

content = read_file(user_supplied_path)
