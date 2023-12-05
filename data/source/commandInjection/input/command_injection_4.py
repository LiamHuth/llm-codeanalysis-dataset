#
#

import os
import subprocess
import sys

class PyShell:
    def __init__(self):
        self.commands = {
            "exit": self.exit_shell,
            "cd": self.change_directory,
            "ls": self.list_directory
        }

    def run(self):
        while True:
            cmd_input = input(" > ")
            cmd_parts = cmd_input.split()
            if not cmd_parts:
                continue
            cmd_name = cmd_parts[0]
            cmd_args = cmd_parts[1:]
            self.execute_command(cmd_name, cmd_args)

    def execute_command(self, cmd_name, cmd_args):
        if cmd_name in self.commands:
            self.commands[cmd_name](cmd_args)
        else:
            self.execute_system_command([cmd_name] + cmd_args)

    def execute_system_command(self, cmd_args):
        if (cmd_args[0] == "rm"):
            print("Error, dangerous command")
            return
        try:
            result = subprocess.run(cmd_args, check=True, text=True, capture_output=True)
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred:", e)
        except FileNotFoundError:
            print("Command not found:", ' '.join(cmd_args))

    def exit_shell(self, args):
        print("Exiting...")
        sys.exit(0)

    def change_directory(self, args):
        if not args:
            return
        try:
            os.chdir(args[0])
        except Exception as e:
            print(f"cd: {e}")

    def list_directory(self, args):
        path = args[0] if args else '.'
        try:
            files = os.listdir(path)
            for file in files:
                print(file)
        except Exception as e:
            print(f"ls: {e}")

if __name__ == "__main__":
    shell = PyShell()
    shell.run()