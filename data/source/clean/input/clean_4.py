# Reference: None
# Dec 4, 2023


import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE name = ?", ("newemail@example.com", "Alice"))
