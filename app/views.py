from flask import render_template, request
from app import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nuevacompra', methods=['GET', 'POST'])
def nuevacompra():
    return render_template('nuevacompra.html')

