import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii_9.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the table

Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
       f" <h1>This is the Weather Analysis Front End Page </h1>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/2014-07-07<br/>"
        f"/api/v1.0/2014-07-07/2015-07-07"
       
    )

@app.route("/api/v1.0/stations")
def names():
    """Return a list of all the stations"""
    # Query all stations
    results = session.query(Station.Station).all()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)


@app.route("/api/v1.0/precipitation")
def precipitation_results():
    """Return a list of all passenger names"""
    # Query all stations
    end_date = session.query(Measurement.Date).order_by(Measurement.Date.desc()).first()
    end_date = np.array(end_date, dtype=np.datetime64)

    start_date = end_date -365
    start_date_str = str(start_date[0])
      
    pcpt_results = session.query(Measurement.Date,Measurement.Temperature ). filter(Measurement.Date > start_date_str).all()
    dict1 = dict(pcpt_results)

    return jsonify(dict1)

@app.route("/api/v1.0/tobs")
def temp_results():
    """Return a list of all passenger names"""
    # Query all stations
    end_date = session.query(Measurement.Date).order_by(Measurement.Date.desc()).first()
    end_date = np.array(end_date, dtype=np.datetime64)

    start_date = end_date -365
    start_date_str = str(start_date[0])
      
    temp_results = session.query(Measurement.Temperature). filter(Measurement.Date > start_date_str).all()
    results_in_a_list = list(np.ravel(temp_results))

    return jsonify(temp_results)

@app.route("/api/v1.0/<start_date1>/<end_date1>")
def calc_temps(start_date1, end_date1):
    data = session.query(Measurement.Temperature). filter(Measurement.Date > start_date1). \
    filter(Measurement.Date < end_date1).all()
    
    mean = np.mean(data)
    max = np.max(data)
    min = np.min(data) 
     
    return jsonify((f"The average temperature is : {mean}, The max temperature is : {max}, The minimum temperature is : {min}")) , 404
 
@app.route("/api/v1.0/<start_date2>")
def calc_temps_with_only_Start_Date(start_date2):
    data = session.query(Measurement.Temperature). filter(Measurement.Date > start_date2).all()
    
    mean = np.mean(data)
    max = np.max(data)
    min = np.min(data) 
     
    return jsonify((f"The average temperature is : {mean}, The max temperature is : {max}, The minimum temperature is : {min}")) , 404 


if __name__ == '__main__':
    app.run(debug=True)