# Author: Zhiqi Zhou
# Date: N/A

username = input("Enter your username: ")
password = input("Enter your password: ")

query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
cursor.execute(query)
