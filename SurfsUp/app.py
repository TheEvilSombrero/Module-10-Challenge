# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
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
    # Return all available API routes 
    return(
        f"<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return JSON representation of the dictionary
    return(
        jsonify()
    )

@app.route("/api/v1.0/stations")
def stations():
    # Return JSON list of stations from the dataset
    return(
        jsonify()
    )

@app.route("/api/v1.0/tobs")
def tobos():
    # Return JSON list of temperature observations for the previous years
    return(
        jsonify()
    )

@app.route("/api/v1.0/<start>")
def start():
    # Calculate TMIN, TAVG, TMAX for all dates >= <start>
    return(
        f"<br/>"
    )

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Calculate TMAG, TAVG, TMAX for all dates >= <start> and <= <end>
    return(
        f"<br/>"
    )