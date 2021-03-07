from flask import Flask, render_template, jsonify,request
from main import stations, next_transports,next_line_station_direction
from station_file_3 import result3
from station_file_1 import result1
from station_file_2 import result2
from flask_cors import CORS
import sqlite3
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/stations')
def entry_point():
    # return render_template('./app.html')
    # return jsonify(stations())
    return render_template('Stations.html',
    blogs=result1)

@app.route('/next/<station>')
def demande(station):
    return jsonify(next_transports(station))
    return render_template('station_next.html',
    blogs1=result2)

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
    app.run(host="0.0.0.0", port="5000", debug=True)