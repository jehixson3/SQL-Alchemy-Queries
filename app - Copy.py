import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

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
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )


@app.route("/api/v1.0/names")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(Passenger.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/passengers")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


if __name__ == '__main__':
    app.run(debug=True)





# import numpy as np
# import pandas as pd
# import datetime as dt
# import sqlalchemy
# from sqlalchemy.ext.automap import automap_base
# from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, func
# from flask import Flask, jsonify

# engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Base = automap_base()
# Base.prepare(engine, reflect=True)

# Measurement = Base.classes.measurement
# Station = Base.classes.station

# session = Session(engine)
# #weather app
# app = Flask(__name__)
# # Get Max Date
# max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
# max_date = list(np.ravel(max_date))[0]
        
# max_date = dt.datetime.strptime(max_date, '%Y-%m-%d')
# #print(max_date)
# #Calculate 1 year from Max Date
# before_date = max_date - dt.timedelta(days=365)

# # 3. Define what to do when a user hits the index route
# @app.route("/")
# def home():
#     return (
#         f"Available Routes:<br/>"
#         f"Welcome to my 'Hawaii Rainfall from 1/1/2010 - 8/32/2017' page!"

#         f"/api/v1.0/precipitation<br/>"
#         f"Dates from the last year 8/2016 - 8/2017"
#         f"-Returns a json list of precipatation by date"

#         f"/api/v1.0/stations<br/>"
#         f"-Returns a json list of stations"
        
#         f"/api/v1.0/tobs<br/>"
#         f"Return a JSON list of Temperature Observations (tobs) for the previous year"

#         f"/api/v1.0/<<br/>"
#         f"Returns minimum temperature, the average temperature, and the max temperature"
#         f" for given date"
        
#         f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
#         f"Returns minimum temperature, the average temperature, and the max temperature"
#         f" for given date range"
#     )        

# @app.route("/api/v1.0/precipitaton")
# def precipitation():
#     results = (session.query(Measurement.date, Measurement.prcp, Measurement.station)
#     .filter(Measurement.date >= before_date )
#     .order_by(Measurement.date)
#     .all())


#     precip = []
#     for result in results:
#         precipDict = {result.date: result.prcp, "Station": result.station}
#         precip.append(precipDict)

#     return jsonify(precip)

# #@app.route("/api/v1.0/stations")
# #def stations():
 
# #     results = session.query(Station.name).all()
# #     stations = list(np.ravel(results))
# #    return jsonify(stations)

# @app.route("/api/v1.0/tobs")
# def temperature():

#     results = (session.query(Measurement.date, Measurement.tobs, Measurement.station)
#         .filter(Measurement.date > before_date)
#         .order_by(Measurement.date)
#         .all())

#     tempData = []
#     for result in results:
#          tempDict = {result.date: result.tobs, "Station": result.station}
#          tempData.append(tempDict)

#     return jsonify(tempData)

# @app.route('/api/v1.0/<date>/')
# def given_date(date):
#     """Return the the min, avg, max for the given date"""
#     results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#     filter(Measurement.date == date).all()

# #Create JSON
#     date_list = []
#     for result in results:
#         dates = {}
#         dates['Date'] = result[0]
#         dates['Lowest Temperature'] = float(result[1])
#         dates['Average Temperature'] = float(result[2])
#         dates['Highest Temperature'] = float(result[3])
#         date_list.append(dates)

#     return jsonify(date_list)

# @app.route('/api/v1.0/<start_date>/<end_date>/')
# def query_dates(start_date, end_date):
#     """Return the min, avg, max, temp over a specific time period"""
#     results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#     filter(Measurement.date >= start_date, Measurement.date <= end_date).all()

#     date_list = []
#     for result in results:
#         dates = {}
#         dates["Start Date"] = start_date
#         dates["End Date"] = end_date
#         dates['Lowest Temperature'] = float(result[1])
#         dates['Average Temperature'] = float(result[2])
#         dates['Highest Temperature'] = float(result[3])
#         date_list.append(dates)
#     return jsonify(date_list)

# if __name__ == "__main__":
#  app.run(host='0.0.0.0', port=5000, debug=True)
