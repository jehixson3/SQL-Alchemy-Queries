# Import Dependencies
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
session = Session(engine)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Get Max and Start date which is 365 days before Max date
max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
max_date = list(np.ravel(max_date))[0]
        
max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
before_date = max_date - dt.timedelta(days=365)

app = Flask(__name__)

# Create home route
@app.route("/")
def home():
    return (
        f"Welcome to my Hawaii Rainfall from 1/1/2010 - 8/32/2017 page!<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"<br/>"
        f"Please paste any of these routes into the browser to access its page.<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"Dates from the last year 8/2016 - 8/2017.<br/>"
        f"-Returns a json list of precipatation by date.<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"-Returns a json list of stations.<br/>"
        f"<br/>"  
        f"/api/v1.0/tobs<br/>"
        f"Return a JSON list of Temperature Observations (tobs) for the previous year.<br/>"
        f"<br/>"
        f"/api/v1.0/start date<br/>"
        f"Returns minimum temperature, the average temperature, and the max temperature<br/>"
        f" for given date please use format yyyy-mm-dd in place of start date, thank you.<br/>"
        f"<br/>"
        f"/api/v1.0/start date/end date/>"
        f"Returns minimum temperature, the average temperature, and the max temperature<br/>"
        f" for given date range please use format yyyy-mm-dd and seperate the dates with a forward /, thank you.<br/>"
    )   
# Routes to create API call precipatation, station and tempature observations and put into json format
@app.route("/api/v1.0/precipitaton")
def precipitation():
    session = Session(engine)
    # results = (session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date >= before_date ).order_by(Measurement.date).all())
    
    lst_year_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= before_date).\
        group_by(Measurement.date).\
        order_by(Measurement.date).all()
    session.close()
    return jsonify(dict(lst_year_prcp))

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)
    results = session.query(Station.station).all()
    session.close()
    return jsonify([station[0] for station in results])

@app.route("/api/v1.0/tobs")
def temperature():
    """Return temperature observations for the last year"""
    session = Session(engine)
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = list(np.ravel(max_date))[0]
        
    max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
    before_date = max_date - dt.timedelta(days=365)

    lst_year_prcp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= before_date).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()
    session.close


    return jsonify(dict(lst_year_prcp))

# Route for when just start date is entered
@app.route("/api/v1.0/<start>")  
def single_date(start):
    """Return the min temp, average temp, and max temp for the date"""
    session = Session(engine)
    strt_dt = dt.datetime.strptime(start, "%Y-%m-%d")
    dates_msr = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= strt_dt).all()
    session.close()

    sum_dt = list(np.ravel(dates_msr))
#Create JSON
    return jsonify(sum_dt)

# Route for when start and end date are supplied
@app.route('/api/v1.0/<start_date>/<end_date>/')
def query_dates(start_date, end_date):
    session = Session(engine)
    start_dt = dt.datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = dt.datetime.strptime(end_date, "%Y-%m-%d")
    """Return the min temp, average temp, and max temp over a specific time period"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_dt, Measurement.date <= end_dt).all()

    date_list = []
    for result in results:
        row = {}
        row["Start Date"] = start_date
        row["End Date"] = end_date
        row["Lowest Temperature"] = float(result[0])
        row["Average Temperature"] = round(float(result[1]))
        row["Highest Temperature"] = float(result[2])
        date_list.append(row)
    return jsonify(date_list)

if __name__ == '__main__':
    app.run(debug=True)
