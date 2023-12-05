#
#

from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <form action="/fileinfo" method="post">
            <input type="text" name="filename" placeholder="Enter filename" />
            <input type="submit" value="Get Info" />
        </form>
    '''

@app.route('/fileinfo', methods=['POST'])
def file_info():
    filename = request.form['filename']
    command = f"ls -l {filename}"
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return f"<pre>{output}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)