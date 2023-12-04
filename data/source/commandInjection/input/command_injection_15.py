# author: Liam Huth
# December 2023

import dill
import os
import sys

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def display_task(self):
        print(f"Task: {self.title}\nDescription: {self.description}")

def save_task(task, filename):
    with open(filename, 'wb') as file:
        dill.dump(task, file)
    print(f"Task '{task.title}' saved.")

def load_task(filename):
    try:
        with open(filename, 'rb') as file:
            task = dill.load(file)
            return task
    except FileNotFoundError:
        print("Task file not found.")

def create_new_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    task = Task(title, description)
    return task

def main_menu():
    print("\n--- Task Manager ---")
    print("1. Create New Task")
    print("2. Load Task")
    print("3. Exit")
    print("--------------------")

def main():
    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            task = create_new_task()
            filename = input("Enter filename to save the task: ")
            save_task(task, filename)
        elif choice == '2':
            filename = input("Enter filename to load the task: ")
            task = load_task(filename)
            if task:
                task.display_task()
        elif choice == '3':
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
