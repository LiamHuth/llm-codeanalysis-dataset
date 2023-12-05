#
#

import os

def emulate_terminal():
    current_directory = os.getcwd()

    while True:
        command = input(f"{current_directory}> ")

        if command == "exit":
            break
        elif command.startswith("cd"):
            directory = command.split(maxsplit=1)[1]
            os.chdir(directory)
            current_directory = os.getcwd()
        else:
            print("Command not recognized or not allowed")

emulate_terminal()
