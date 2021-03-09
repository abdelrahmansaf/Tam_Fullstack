from flask import Flask, render_template, jsonify,request
from main import stations, next_transports,next_line_station_direction,Ligne,ligne_search
from flask_cors import CORS
import sqlite3
from main import main, update_db, load_csv, create_schema, insert_csv_row
from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(daemon=True)
sched.add_job(main,'interval',seconds= 59)
sched.start()
app = Flask(__name__)
CORS(app)
main()

@app.route('/')
def home():
    stations()
    return render_template('home.html',title='Welcome')

@app.route('/stations')
def entry_point():
    return jsonify(stations())
    


@app.route('/next/<station>')
def demande(station):
    return jsonify(next_transports(station))

@app.route('/line')
def ligne_list():
    return jsonify(Ligne())    

@app.route('/line/<ligne>')
def demande_ligne(ligne):
    return jsonify(ligne_search(ligne))

@app.route('/next', methods=['GET'])
def next_infos():

    args1 = request.args['Ligne']
    args2 = request.args['Station']
    args3 = request.args['Direction']
    return jsonify(next_line_station_direction(args1,args2,args3))
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=True)


