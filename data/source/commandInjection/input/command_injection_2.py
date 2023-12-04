#
#

from flask import Flask, request
import subprocess

app = Flask(__name__)

def getCommand():
    c = request.args.get('command')
    if (c[:2] == "rm" or c[:2] == "cd"):
        return ""
    return c

@app.route('/run')
def run_command():
    command = getCommand()
    if (command == ""):
        return "invalid"
    else:
        subprocess.run(command, shell=True)
        return "success"

