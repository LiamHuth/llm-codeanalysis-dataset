#
#

def readSqliteTable():
    try:
        sqliteConnection = sqlite3.connect('User.db')
        cursor = sqliteConnection.cursor()

        sqlite_select_query = "SELECT * from users"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
      

        cursor.close()

    except sqlite3.Error as error:
        ...
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def login(username, password):
    try:
        sqliteConnection = sqlite3.connect('User.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_query = "SELECT * from users where username='" + username + "'" + " AND password='" + password + "';" 
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
    except sqlite3.Error as error:
        ...
    finally:
        if sqliteConnection:
            sqliteConnection.close()
