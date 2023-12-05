# Reference: https://knowledge-base.secureflag.com/vulnerabilities/sql_injection/sql_injection_python.html
# Date: N/A

@app.route("/login")
def login():
    username = request.values.get('username')
    password = request.values.get('password')

    db = pymysql.connect("localhost")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE username = '%s' AND password = '%s'" % (username, password))

    record = cursor.fetchone()
    if record:
        session['logged_user'] = username

    db.close()