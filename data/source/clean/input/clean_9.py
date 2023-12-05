#
#

import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    search_term = "%coffee%"
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", (search_term,))
