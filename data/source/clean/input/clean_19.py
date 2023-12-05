#
#

import subprocess

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        print(f"Output:\n{result}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def main():
    whitelist_commands = {
        '1': 'ls',
        '2': 'whoami',
        '3': 'date',
    }

    while True:
        for key, cmd in whitelist_commands.items():
            print(f"{key}. {cmd}")
        print("0. Exit")


        choice = input("Enter your choice: ")

        if choice == '0':
            print("Exiting...")
            break
        elif choice in whitelist_commands:
            execute_command(whitelist_commands[choice])
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
