# Reference: https://www.codiga.io/blog/python-prevent-sql-injection/
# Date: N/A

import mysql.connector

def get_user(customer_id):
  mydb = mysql.connector.connect(...)
  mycursor = mydb.cursor()
  mycursor.execute(f"SELECT * FROM customers WHERE id={customer_id}")