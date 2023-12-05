# author: Liam Huth
# December 2023

from flask import Flask, request, render_template_string
import hashlib

app = Flask(__name__)

def generate_hash(num):
    sha_signature = hashlib.sha256(str(num).encode()).hexdigest()
    return sha_signature

@app.route('/', methods=['GET', 'POST'])
def index():
    hash_result = None
    if request.method == 'POST':
        try:
            number = int(request.form.get('number'))
            hash_result = generate_hash(number)
            return f"<pre>{hash_result}</pre>"
        except ValueError:
            hash_result = "Invalid input. Please enter an integer."

    return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Integer Hash Generator</title>
        </head>
        <body>
            <h2>Enter a number to generate its SHA-256 hash:</h2>
            <form method="post">
                <input type="text" name="number" />
                <input type="submit" value="Generate Hash" />
            </form>
            {% if hash_result %}
                <h3>Hashed Value: {{ hash_result }}</h3>
            {% endif %}
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(debug=True)
