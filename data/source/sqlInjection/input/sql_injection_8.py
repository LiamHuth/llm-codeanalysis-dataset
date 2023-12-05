#
#

import mysql.connector
def search_user(username):
    conn = mysql.connector.connect(user='root', password='password', host='localhost', database='users')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    return result