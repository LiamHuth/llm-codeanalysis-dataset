#
#

import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    users = [("Charlie", "charlie@example.com"), ("Dave", "dave@example.com")]
    cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)