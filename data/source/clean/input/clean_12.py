# Reference: None
# Dec 4, 2023

safe_files = {
    "file1": "/safe/directory/file1.txt",
    "file2": "/safe/directory/file2.txt",
}

def read_file(file_key):
    if file_key in safe_files:
        with open(safe_files[file_key], 'r') as file:
            return file.read()
    else:
        raise ValueError("File not found.")

content = read_file(user_supplied_key)
