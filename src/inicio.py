from flask import Flask, render_template

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/reload')
def hello_world2():
    return 'Hello, World!'
