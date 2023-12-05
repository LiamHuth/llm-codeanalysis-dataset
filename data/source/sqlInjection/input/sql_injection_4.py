# Author: Zhiqi Zhou
# Date: N/A

item = input("Enter the item you're looking for: ")

query = "SELECT * FROM inventory WHERE item_name = '" + item + "'"
cursor.execute(query)
