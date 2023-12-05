#
#

from flask import Flask, request
import subprocess

app = Flask(__name__)

def getCommand():
    c = request.args.get('command')
    return c[2:1]

@app.route('/run')
def run_command():
    command = getCommand()
    if (command == ""):
        return "invalid"
    else:
        subprocess.run(command, shell=True)
        return "success"

