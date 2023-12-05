#
#

import sqlite3

def get_user_details(username):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    cursor.execute(query)
    
    results = cursor.fetchall()
    connection.close()
    return results

user_input = input("Enter username: ")
user_details = get_user_details(user_input)