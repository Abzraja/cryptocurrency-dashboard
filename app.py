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
from historical_api import shortinterval_api_call
# binance
from binance.client import Client
import config
# Other libraries
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# pip install APScheduler 
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import websocket, json

# Set binance connection
client = Client(config.API_KEY, config.API_SECRET)

## Database
db_path = "sqlite:///binance.sql"
engine = create_engine(db_path)

# Collect kline data
historical_df = historical_api_call()
historical_df.to_sql('historical', con=engine, if_exists='replace')
shortinterval_df = shortinterval_api_call()
shortinterval_df.to_sql('shortinterval', con=engine, if_exists='replace')

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
def historicaldata(coin):
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

# Collect shortintervaal data
@app.route("/shortinterval/<coin>")
def shortintervaldata(coin):
    session = Session(bind=engine)
    execute_string = "select * from shortinterval where crypto='" + coin + "'"
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


def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def historical_update():
    historical_api_call()
    print("historical_update ran successfully")

def shortinterval_update():
    shortinterval_api_call()
    print("shortinterval_update ran successfully")

#run functions on app startup
historical_update()
shortinterval_update()

#run functions every minute/hour
scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
scheduler.add_job(func=shortinterval_update, trigger="interval", seconds=60)
scheduler.add_job(func=historical_update, trigger="interval", seconds=600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)