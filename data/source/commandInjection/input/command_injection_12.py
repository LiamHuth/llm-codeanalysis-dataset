#
#

from flask import Flask, request, render_template_string, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'OusxbRGeoHPb7oVFjG2NOSsbjcujowhf'

# Database setup
DATABASE = 'app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return '''
        <h1>Welcome to the Advanced Settings App</h1>
        <a href="/setpath">Modify PATH</a><br>
        <a href="/profile">Profile Settings</a><br>
        <a href="/logout">Logout</a>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db_connection()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()

        if user and check_password_hash(user['password'], password):
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'

    return '''
        <form method="post">
            <p><input type=text name=username placeholder="Username"></p>
            <p><input type=password name=password placeholder="Password"></p>
            <p><input type=submit value=Login></p>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return '<h1>User Profile Page</h1>'

@app.route('/setpath', methods=['GET', 'POST'])
def set_path():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_path = request.form['newpath']
        original_path = os.environ.get('PATH')
        os.environ['PATH'] = new_path + ":" + original_path
        return f"PATH has been updated. New PATH: {os.environ.get('PATH')}"

    return '''
        <form method="post">
            <p><input type=text name=newpath placeholder="Enter new PATH value"></p>
            <p><input type=submit value="Set PATH"></p>
        </form>
    '''

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    # Admin-only functionality
    return '<h1>Admin Dashboard</h1>'

if __name__ == '__main__':
    init_db()
    app.run(debug=True)