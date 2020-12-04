from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/home')
def sano_bot():
    return render_template('index.html')
app.run(host='0.0.0.0', port=8080)