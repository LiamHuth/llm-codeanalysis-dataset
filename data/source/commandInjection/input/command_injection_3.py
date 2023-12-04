# author: Liam Huth
# December 2023

def clean(s):
    # sanitize the data
    if (s[:2] == "ls" or \
        s[:2] == "rm" or \
        s[:2] == "ls" or \
        s[:5] == "mkdir"):
        return ""
    return s

def getFileInfo():
    file_name = clean(input("name: "))
    file_contents = clean(input("file content: "))
    return file_name, file_contents

def main():
    name, content = getFileInfo()
    if (name == "" or content == ""):
        print("Could not create file")
    else:
        with open(name, 'w') as newFile:
            newFile.write(content)