#
#

import mysql.connector

def get_user(customer_id):
  mydb = mysql.connector.connect(...)
  mycursor = mydb.cursor()
  mycursor.execute(f"SELECT * FROM customers WHERE id={customer_id}")