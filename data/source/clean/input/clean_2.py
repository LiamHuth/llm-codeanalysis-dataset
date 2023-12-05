#
#

import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = :name", {"name": "Alice"})
