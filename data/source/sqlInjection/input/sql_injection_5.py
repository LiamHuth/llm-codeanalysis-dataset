# Author: Zhiqi Zhou
# Date: N/A

email = input("Enter your email to check for subscription status: ")

query = f"SELECT * FROM subscribers WHERE email = '{email}'"
cursor.execute(query)
