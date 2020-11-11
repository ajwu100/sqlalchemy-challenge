import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import Column, Integer, String, Float
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
# Save references to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Flask Setup
app = Flask(__name__)

# Flask Routes


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<START_DATE><br/>"
        f"/api/v1.0/<START_DATE>/<END_DATE><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Measurement for date and prcp
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_prcp
    all_prcp = []
    for date, prcp in prcp_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station_data = session.query(Measurement.station).all()
    session.close()

    station_list = list(np.ravel(station_data))
    unique_stations = []
    for station in station_list:
        if station not in unique_stations:
            unique_stations.append(station)

    return jsonify(unique_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    temps_USC00519281 = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= '2016-08-23').\
        filter(Measurement.date <= '2017-08-23').all()
    temps_list = list(np.ravel(temps_USC00519281))

    return jsonify(temps_list)


@app.route("/api/v1.0/<START_DATE>")
def temp_page(START_DATE):
    session = Session(engine)
    mintemp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= START_DATE).\
        filter(Measurement.date <= "2017-08-23").all()
    maxtemp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= START_DATE).\
        filter(Measurement.date <= "2017-08-23").all()
    avgtemp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= START_DATE).\
        filter(Measurement.date <= "2017-08-23").all()
    session.close()

    return jsonify(mintemp, maxtemp, avgtemp)


@app.route("/api/v1.0/<START_DATE>/<END_DATE>")
def temps_page(START_DATE, END_DATE):
    session = Session(engine)
    mintemp = session.query(func.min(Measurement.tobs)).\
        filter(Measurement.date >= START_DATE).\
        filter(Measurement.date <= END_DATE).all()
    maxtemp = session.query(func.max(Measurement.tobs)).\
        filter(Measurement.date >= START_DATE).\
        filter(Measurement.date <= END_DATE).all()
    avgtemp = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= START_DATE).\
        filter(Measurement.date <= END_DATE).all()
    session.close()

    return jsonify(mintemp, maxtemp, avgtemp)


if __name__ == "__main__":
    app.run(debug=True)
