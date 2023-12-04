# written by Liam Huth, reference: https://davidhamann.de/2020/04/05/exploiting-python-pickle/
# December 2023

import pickle
import base64
import os

class UserPreferences:
    def __init__(self, username, preferences):
        self.username = username
        self.preferences = preferences

    def save_preferences(self):
        # Serialize and encode the preferences
        serialized_data = pickle.dumps(self)
        encoded_data = base64.b64encode(serialized_data).decode('utf-8')
        with open(f"{self.username}_prefs", "w") as file:
            file.write(encoded_data)

    @staticmethod
    def load_preferences(username):
        try:
            with open(f"{username}_prefs", "r") as file:
                encoded_data = file.read()
                serialized_data = base64.b64decode(encoded_data)
                # Deserialize the preferences
                return pickle.loads(serialized_data)
        except FileNotFoundError:
            print("Preferences file not found.")

def main():
    print("User Preferences Manager")
    username = input("Enter your username: ")

    # Check if the user has saved preferences
    if os.path.exists(f"{username}_prefs"):
        user_prefs = UserPreferences.load_preferences(username)
        print(f"Loaded preferences for {user_prefs.username}: {user_prefs.preferences}")
    else:
        # Create new preferences
        preferences = {"theme": "light", "notifications": True}
        user_prefs = UserPreferences(username, preferences)
        user_prefs.save_preferences()
        print("Preferences saved.")

if __name__ == "__main__":
    main()
