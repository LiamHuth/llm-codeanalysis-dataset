# Reference: None
# Dec 4, 2023

import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    new_user = ("Bob", "bob@example.com")
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", new_user)