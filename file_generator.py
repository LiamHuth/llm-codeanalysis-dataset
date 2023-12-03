
vul_type = "sql_injection_"
file_type = ".py"

for i in range(8, 26):
    directory = "./data/source/sqlInjection/input/" + vul_type + str(i) + file_type
    with open(directory, 'w') as file:
        pass
