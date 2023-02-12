from flask import Flask

app = Flask(__name__)

@app.route('/<int:number>/')
def display(number):
    return f"<p>You requested {number}!</p>"

@app.route("/")
def hello_world():
    return "<p>Hello, World 222!</p>"