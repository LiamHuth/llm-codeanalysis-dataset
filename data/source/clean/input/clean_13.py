# Reference: None
# Dec 4, 2023

from pathlib import Path

def read_file(user_input, base_directory=Path("/safe/directory")):
    full_path = (base_directory / user_input).resolve()

    if base_directory in full_path.parents:
        with open(full_path, 'r') as file:
            return file.read()
    else:
        raise ValueError("Access denied.")

content = read_file(user_supplied_path)
