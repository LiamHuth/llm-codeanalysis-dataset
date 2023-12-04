# Reference: None
# Dec 4, 2023

import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()

    user_id = 123
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))