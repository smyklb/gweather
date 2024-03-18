import datetime
import requests
from flask import Flask, render_template, request
from datetime import datetime
from matplotlib import pyplot as plt

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)