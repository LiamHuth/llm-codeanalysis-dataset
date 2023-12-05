#
#

file_map = {
    "key1": "/safe/directory/file1.txt",
    "key2": "/safe/directory/file2.txt",
}

def read_file(file_key):
    if file_key in file_map:
        with open(file_map[file_key], 'r') as file:
            return file.read()
    else:
        raise ValueError("Invalid file key.")

content = read_file(user_supplied_key)
