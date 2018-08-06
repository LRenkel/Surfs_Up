from flask import Flask, jsonify

from dbsetup import session, Measurement, Station, engine, func


app = Flask(__name__)
@app.route('/')
def home_route():
    return "This is the homepage for Surf's Up"

@app.route('/api/v1.0/precipitation/')
def precipv1():
    precip = session.query(Measurement.date, Measurement.prcp)\
        .filter(Measurement.date.between('2017-01-01', '2017-12-31'))\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)
    precip_vals = {k:v for k,v in precip}
    return jsonify(precip_vals)

@app.route('/api/v1.0/stations/')
def station_route():
    station_list = {}
    station_list['data'] = []
    
    for row in session.query(Station):
        station_list['data'].append(
            {"id": row.id, 
            'station': row.station, 
            "lat": row.latitude,
            "lng": row.longitude,
            "elev": row.elevation}  
        )
    return jsonify(station_list)

@app.route('/api/v1.0/tobs/')
def temp_obs():
    tobs = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.date.between('2017-01-01', '2017-12-31'))\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)
    vals = {k:v for k,v in tobs}
    return jsonify(vals)

@app.route('/api/v1.0/<start>/<end>/')
def start_end(start, end):
    tobs_calcs = session.query(func.avg(Measurement.tobs).label('avg_temp'), 
                               func.min(Measurement.tobs).label('min_temp'),
                               func.max(Measurement.tobs).label('max_temp'))\
                               .filter(Measurement.date.between(f'{start}', f'{end}'))
    tobs_list = {}
    tobs_list['data'] = []
    for row in tobs_calcs:
        tobs_list['data'].append(
        {"Avg Temp": row.avg_temp, 
         'Min Temp': row.min_temp, 
         "Max Temp": row.max_temp})
    return jsonify(tobs_list['data'])

@app.route('/api/v1.0/<start>/')
def start_date(start):
    tobs_calcs = session.query(func.avg(Measurement.tobs).label('avg_temp'), 
                               func.min(Measurement.tobs).label('min_temp'),
                               func.max(Measurement.tobs).label('max_temp'))\
                               .filter(Measurement.date >= f'{start}')
    tobs_list = {}
    tobs_list['data'] = []
    for row in tobs_calcs:
        tobs_list['data'].append(
        {"Avg Temp": row.avg_temp, 
         'Min Temp': row.min_temp, 
         "Max Temp": row.max_temp})
    return jsonify(tobs_list['data'])

app.run(debug=True)