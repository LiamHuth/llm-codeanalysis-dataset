# Reference: None
# Dec 4, 2023

import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT users.name, orders.amount 
    FROM users 
    JOIN orders ON users.id = orders.user_id 
    WHERE users.id = %s
    """, (user_id,))