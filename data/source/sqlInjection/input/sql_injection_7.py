#
#

import mechanize

url = input("Enter the full url")

with open ("vectors.txt") as v:
    for line in v:
        browser.open(url)
        browser.select_form(nr = 0)
        browser["id"] = line
        res = browser.submit()

content = res.read()
output = open("response/" + str(num) + ".txt", "w")
output.write(content)
output.close()
print(num)
num += 1