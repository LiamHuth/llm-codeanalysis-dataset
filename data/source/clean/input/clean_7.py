#
#

import datetime
import sqlite3

def main():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    date = datetime.date.today()
    cursor.execute("SELECT * FROM events WHERE date = ?", (date,))
