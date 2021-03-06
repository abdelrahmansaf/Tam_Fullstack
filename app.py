from flask import Flask, render_template, jsonify,request
from main import stations, next_transports,next_line_station_direction
import sqlite3
app = Flask(__name__)


@app.route('/')
def home():
    return jsonify('Hello, World!')

@app.route('/stations')
def entry_point():
    # return render_template('./app.html')
    return jsonify(stations())

@app.route('/next/<station>')
def demande(station):
    return jsonify(next_transports(station))

# @app.route('/next/<line>/<station>/<direction>')
# def next_infos(line,station,direction):
#     return jsonify(next_line_station_direction(line,station,direction))

@app.route('/next', methods=['GET'])
def next_infos():

    args1 = request.args['Ligne']
    args2 = request.args['Station']
    args3 = request.args['Direction']

    return jsonify(next_line_station_direction(args1,args2,args3))


if __name__ == '__main__':
    app.run(debug=True)