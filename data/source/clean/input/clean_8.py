#
#


import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE price > ? AND in_stock = ?", (price, True))
