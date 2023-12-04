# Reference: https://github.com/yi-jiayu/sqli-example/blob/master/app.py
# Date: May 18, 2018

def login(username, password):
    conn = db.connect()
    query = db.build_query(username, password)
    c = conn.cursor()
    c.execute(query)
    row = c.fetchone()
    conn.close()
    if row is not None:
        return row[0]
    else:
        return None

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def dashboard():
    username, password = request.form['username'], request.form['password']
    username = login(username, password)
    if username:
        return render_template('dashboard.html', username=username)
    else:
        return render_template('index.html', message='Login failed!')