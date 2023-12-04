# Implicit SQL Injection by CHATGPT 4.0
# Date: N/A

import sqlite3

# Function to get user details
def get_user_details(username):
    # Connect to the SQLite database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Constructing SQL query using string formatting with user input
    query = f"SELECT * FROM users WHERE username = '{username}'"
    




    
    # Executing the query
    cursor.execute(query)
    
    # Fetching the results
    results = cursor.fetchall()
    connection.close()
    return results

# Example of getting user details
# The username is provided by the user (e.g., through input or web request)
user_input = input("Enter username: ")
user_details = get_user_details(user_input)
print(user_details)