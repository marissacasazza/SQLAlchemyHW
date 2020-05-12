
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
#station,date,prcp,tobs
Measurement = Base.classes.measurement
#station,name,latitude,longitude,elevation
Station = Base.classes.station


#Flask Setup
app = Flask(__name__)

def calc_temps(start_date, end_date = "None"):
    session = Session(engine)
    if end_date != "None":
        data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    else:
        data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    session.close()

    return data


@app.route("/")
def climate():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    data = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= '2016-08-23').order_by(Measurement.date).all()

    session.close()
    
    data_df = list(np.ravel(data))

    return jsonify(data_df)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    data = session.query(Station.station).all()
    session.close()

    data_df = list(np.ravel(data))

    return jsonify(data_df)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
  
    data = session.query(Measurement.tobs)\
        .filter(Measurement.station == 'USC00519281').all()
    df2 = pd.DataFrame(data)

    return jsonify(df2.to_dict("records"))

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
  
    data = calc_temps(start)

    
    data_df = list(np.ravel(data))

    return jsonify(data_df)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
  
    data = calc_temps(start, end)

 
    data_df = list(np.ravel(data))

    return jsonify(data_df)


if __name__ == '__main__':
    app.run(debug=True)
