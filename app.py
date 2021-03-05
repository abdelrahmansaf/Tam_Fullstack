from flask import Flask, render_template, jsonify
from main import stations, next_transports
import sqlite3
app = Flask(__name__)

@app.route('/stations')
def entry_point():
    # return render_template('./app.html')
    return jsonify(stations())

@app.route('/stations/<station>')
def demande(station):
    return jsonify(next_transports(station))

if __name__ == '__main__':
    app.run(debug=True)