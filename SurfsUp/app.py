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
        f"Available routes:<br/>"
        f"Homepage: '/' <br/>"
        f"Precipitation data: '/api/v1.0/precipitation' <br/>"
        f"Station data: '/api/v1.0/stations' <br/>"
        f"Temperature observations: '/api/v1.0/tobs' <br/>"
        f"Minimum, maximum, and average temperatures from start date: '/api/v1.0/<start>' <br/>"
        f"Enter desired start date in 'YYYY-MM-DD' format inside <start> without the carrots (<>) <br/>"
        f"Minimum, maximum, and average temperatures between the specified start and end dates: '/api/v1.0/<start>/<end>' <br/>"
        f"Enter desired dates in 'YYYY-MM-DD' format inside <start>/<end> without the carrots (<>) <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return JSON representation of the dictionary
    
    # Pull most recent date - hard coded because the dataset is not changing 
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    most_recent_date = dt.date(2017, 8, 23)
    
    # Calculate one year ago from the most recent date 
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Pull relevant data from the specified timeframe 
    rain_results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
                        filter(Measurement.date >= one_year_ago).all()
    
    return(jsonify(rain_results))

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
    # Calculate TMIN, TMAX, TAVG for all dates >= <start>
    return(
        f"<br/>"
    )

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    # Calculate TMAG, TMAX, TAVG for all dates >= <start> and <= <end>
    return(
        f"<br/>"
    )