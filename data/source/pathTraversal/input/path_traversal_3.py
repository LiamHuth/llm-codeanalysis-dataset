#
#

from flask import Flask, render_template

app = Flask(__name__, static_folder='./www', template_folder='./www')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/home')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=3003)