# author: Liam Huth
# December 2023

import os
import subprocess
import sys

def print_menu():
    print("\n--- Simple File Management System ---")
    print("1. List Files")
    print("2. Read File Contents")
    print("3. Delete File")
    print("4. Execute a System Command")
    print("5. Exit")
    print("------------------------------------")

def sanitize(s):
    if (s[:2] == "rm"):
        return ""
    return s

def list_files(directory):
    try:
        files = os.listdir(directory)
        if not files:
            print("No files found.")
        for file in files:
            print(file)
    except FileNotFoundError:
        print("Directory not found.")

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            print(file.read())
    except FileNotFoundError:
        print("File not found.")

def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"File {file_path} deleted.")
    except FileNotFoundError:
        print("File not found.")

def execute_system_command(command):
    command = sanitize(command)
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            directory = input("Enter directory to list files: ")
            list_files(directory)
        elif choice == '2':
            file_path = input("Enter file path to read contents: ")
            read_file(file_path)
        elif choice == '3':
            file_path = input("Enter file path to delete: ")
            delete_file(file_path)
        elif choice == '4':
            command = input("Enter system command to execute: ")
            execute_system_command(command)
        elif choice == '5':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()