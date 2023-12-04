# Reference: https://brightsec.com/blog/directory-traversal/ (converted to Python with ChatGPT)
# Date: Dec 3, 2023

from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    design = 'new-design.html'
    template = request.cookies.get('DESIGN', design)
    return open(f"../resources/{template}").read()

if __name__ == '__main__':
    app.run(debug=True)