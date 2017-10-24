from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/transform/')
def transform():
    return render_template('index.html')
