# Reference: https://github.com/python-security/pyt/blob/master/examples/vulnerable_code/path_traversal.py
# Apr 14, 2018

import os
from flask import Flask, request, send_file

app = Flask(__name__)

def outer(outer_arg, other_arg):
	outer_ret_val = outer_arg + 'hey' + other_arg
	return outer_ret_val

def inner():
	return 'boom'

@app.route('/')
def cat_picture():
    image_name = request.args.get('image_name')
    if not image_name:
        image_name = 'foo'
        return 404
    foo = outer(inner(), image_name)
    send_file(foo)
    return 'idk'

if __name__ == '__main__':
    app.run(debug=True)

