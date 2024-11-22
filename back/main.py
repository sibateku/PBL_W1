# coding: utf-8

from flask import Flask
import account

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/ja')
def hello_world_ja():
    return 'こんにちは 世界！'

if __name__ == '__main__':
    app.run(debug=True)