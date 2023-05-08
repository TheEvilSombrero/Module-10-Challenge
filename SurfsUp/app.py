# Import the dependencies.
import numpy as np
import datetime as dt

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
        f"Available routes: <br/>"
        f"Homepage: '/' <br/>"
        f"Precipitation data: '/api/v1.0/precipitation' <br/>"
        f"Station data: '/api/v1.0/stations' <br/>"
        f"Temperature observations: '/api/v1.0/tobs' <br/>"
        f"Minimum, maximum, and average temperatures from start date: '/api/v1.0/start' <br/>"
        f"Enter desired start date in 'YYYY-MM-DD' format inside start without the carrots (<>) <br/>"
        f"Minimum, maximum, and average temperatures between the specified start and end dates: '/api/v1.0/start/end' <br/>"
        f"Enter desired dates in 'YYYY-MM-DD' format inside <start>/<end> without the carrots (<>) <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Return JSON representation of the dictionary
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Pull most recent date - hard coded because the dataset is not changing 
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    most_recent_date = dt.date(2017, 8, 23)
    
    # Calculate one year ago from the most recent date 
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Pull relevant data from the specified timeframe 
    rain_results = session.query(Measurement.date, Measurement.prcp).\
                        filter(Measurement.date >= one_year_ago).all()
    
    # Put results into list for JSONIFY 
    
    # Put into dictionary for display 
    rain_results_dict = {}
    for r in rain_results:
        rain_results_dict[r[0]] = r[1]
    
    # Close session
    session.close()
    
    return(jsonify(rain_results_dict))
# Cannot JSONIFY this
# TypeError: Object of type Row is not JSON serializable

@app.route("/api/v1.0/stations")
def stations():
    # Return JSON list of stations from the dataset
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query all of the stations and turn it into a list
    results = session.query(Station.station).all()
    stations_list = list(np.ravel(results))
    
    # Close session
    session.close()
    
    return(jsonify(stations_list))

@app.route("/api/v1.0/tobs")
def tobos():
    # Return JSON list of temperature observations for the previous years
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Get date one year before most recent data point 
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    most_recent_date = dt.date(2017, 8, 23)
    one_year_ago = most_recent_date - dt.timedelta(days=365)
    
    # Get most active station 
    most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
                                    group_by(Measurement.station).\
                                    order_by(func.count(Measurement.station).desc()).all()
    
    most_active_station = most_active_stations[0][0]
    most_active_station_temp = session.query(Measurement.tobs).\
                                filter(Measurement.date >= one_year_ago).\
                                filter(Measurement.station == most_active_station).all()
    
    most_active_station_list = list(np.ravel(most_active_station_temp))
    
    # Close session
    session.close()
    
    return(jsonify(most_active_station_list))

@app.route("/api/v1.0/<start>")
def start(start):
    # Calculate TMIN, TMAX, TAVG for all dates >= <start>
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Turn start time into DT format    
    start_date = dt.datetime.strptime(start, "%Y%m%d")
    
    # Query min, max, avg for all dates >= start_date
    temp_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date).all()
    
    # Format query 
    temp_list = list(np.ravel(temp_query))
    
    # Close session
    session.close()
    
    return(jsonify(temp_list))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Calculate TMAG, TMAX, TAVG for all dates >= <start> and <= <end>
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Turn start time into DT format    
    start_date = dt.datetime.strptime(start, "%Y%m%d")
    end_date = dt.datetime.strptime(end, "%Y%m%d")
    
    # Query min, max, avg for all dates >= start_date
    temp_query = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
                            filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date).all()
    
    # Format query 
    temp_list = list(np.ravel(temp_query))
    
    # Close session
    session.close()
    
    return(jsonify(temp_list))

if __name__ == '__main__':
    app.run(debug=True)