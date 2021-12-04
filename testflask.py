from flask_cors import CORS
from flask import Flask

app = Flask(__name__)
CORS(app) #Prevents CORS errors 


@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = 8000)
