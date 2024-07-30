from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to the Flask app!'

@app.route('/hello')
def hello():
    return 'Hello, world!'

if __name__ == '__main__':
    port = os.getenv('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)