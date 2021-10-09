# Import Flask
from os import replace
from flask import Flask, jsonify, render_template
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
# Import data collection needs
import sqlite3 as sql
import pandas as pd
from historical_api import historical_api_call
# binance
from binance.client import Client
import config
# Other libraries
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Set binance connection
client = Client(config.API_KEY, config.API_SECRET)

## Database
db_path = "sqlite:///binance.sql"
engine = create_engine(db_path)

# Collect historical data
historical_df = historical_api_call()
historical_df.to_sql('historical', con=engine, if_exists='replace')

# Set app name as "app" and start Flask
app = Flask(__name__)

# Base route
@app.route("/")
# Return static HTML file with JS code
# Ideally would serve from independent web server, but not practical in test environment
def home():
    return render_template ("test.html")

@app.route("/sumtrades")
def sumtrades():
    session = Session(bind=engine)
    execute_string = "select crypto, sum(trade) from historical group by crypto"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    coin_dict = {}
    for row in coins:
        print(row)
        coin_dict[row[0]] = row[1]
        print (coin_dict)
    
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))    

# API call to return volume and trades for all coins
@app.route("/linechart")
def line():
    session = Session(bind=engine)
    execute_string = "select * from historical"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    coin_dict = {}
    for row in coins:
        coin_dict[row[0]] = ({
            "crypto": row[1],
            "date": row[2],
            "volume": row[7],
            "trade": row[8]
            })
    
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))


# API call to return all data for one coin
@app.route("/historical/<coin>")
def data(coin):
    session = Session(bind=engine)
    execute_string = "select * from historical where crypto='" + coin + "'"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    coin_dict = {}
    for row in coins:
        coin_dict[row[0]] = ({
            "crypto": row[1], 
            "date": row[2],
            "open": row[3],
            "high": row[4],
            "low": row[5],
            "close": row[6],
            "volume": row[7],
            "number_trades": row[8]
            })
    
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))


# Historical chart page
@app.route("/historical")
def chart():
    return render_template ("historical.html")

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)