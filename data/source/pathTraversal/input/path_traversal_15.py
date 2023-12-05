# Author: Zhiqi Zhou
# Date: Dec 3, 2023

from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    directory = request.form['directory']
    file_path = os.path.join('/uploads', directory, file.filename)
    file.save(file_path)

if __name__ == '__main__':
    app.run(debug=True)