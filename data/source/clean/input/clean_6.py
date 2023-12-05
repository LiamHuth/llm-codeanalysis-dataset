#
#

import psycopg2

def main():
    conn = psycopg2.connect("dbname=testdb user=postgres")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
