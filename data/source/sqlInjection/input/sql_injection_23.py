# Reference: https://github.com/DavidAbderhalden/Example_SQL_Injection/blob/main/Example_SQL_Injection/main.py
# Date: Nov 23, 2020

@app.route('/index', methods=['POST', 'GET'])
def login():
    if 'name' in session:
        table = (mydata.list_converter())
        return render_template("index.html", name=escape(session['name']), password=escape(session['password']), table=table)
    else:
        return render_template("login.html")


app.secret_key = "b'\xba\x9d\xa4oBU\x8d/\x96\xe1\x04\x0e\xb3\xc6\xd5\xca\x88\r$\x10\xa3\xf2i\x9a'"


@app.route("/login", methods=['POST', 'GET'])
def sessions_login():
    if request.method == 'POST':
        if mydata.login_checker_injectable(request.form['username'], request.form['password']):
            print("Login = True")
            session['name'] = request.form['username']
            session['password'] = request.form['password']
            return redirect(url_for('login'))
        else:
            print(False)
            return redirect(url_for('login'))


@app.route("/register", methods=['POST', 'GET'])
def sessions_register():
    if request.method == 'POST':
        # check if data already exists.
        if request.form['username'] =='' or request.form['password'] =='':
            return redirect(url_for('login'))
        else:
            if not mydata.login_checker_safe(request.form['username'], request.form['password']):
                session['name'] = request.form['username']
                session['password'] = request.form['password']
                mydata.register(escape(session['name']), escape(session['password']))
                return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('name', None)
    return redirect(url_for('login'))


@app.route('/favicon.ico')
def fav():
    return send_from_directory(os.path.join(app.root_path, 'img'),'favicon.ico')
