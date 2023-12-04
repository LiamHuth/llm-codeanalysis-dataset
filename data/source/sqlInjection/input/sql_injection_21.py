# Reference: https://github.com/AVVasiliev/sql-injections/blob/main/server/models.py
# Date: Oct 8, 2020

class Database:
    table_name = ""
    def __init__(self, db_path: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "db.sql")):
        self.db_path = db_path
    def __enter__(self):
        self.db_conn = sqlite3.connect(self.db_path)
        self.cursor = self.db_conn.cursor()
        return self
    def __exit__(self):
        self.db_conn.commit()
        self.db_conn.close()
    @exception_pass
    def filter_by(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchall()
    @exception_pass
    def find_one(self, field, value):
        self.cursor.execute(f"SELECT * from {self.table_name} WHERE {field} = '{value}'")
        return self.cursor.fetchone()
    @exception_pass
    def add(self, *values):
        add_values = f"INSERT INTO {self.table_name} VALUES ("
        for v in values:
            add_values += f"'{v}', "
        add_values = add_values[:len(add_values)-2] + ")"
        self.cursor.execute(add_values)
    def __del__(self):
        self.db_conn.close()

class User(Database):
    table_name = "users"
    @exception_pass
    def _create_table(self):
        self.cursor.execute(
            f"""CREATE TABLE {self.table_name} (id text, username text, mail text, password text, superuser bit)""")
        self.db_conn.commit()
    @exception_pass
    def find_user(self, username, password):
        self.cursor.execute(f"SELECT username, mail from {self.table_name} WHERE username = '{username}' and password = '{password}'")
        return self.cursor.fetchone()
    def is_admin(self, username):
        user = self.find_one("username", username)
        if user and user[-1] == 1:
            return True
        return False
    @exception_pass
    def get_users(self, username):
        if not self.is_admin(username):
            return []
        self.cursor.execute(f"SELECT id username mail from {self.table_name}")
        return self.cursor.fetchall()