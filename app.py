# Import Flask
import os
from flask import Flask, jsonify, render_template, redirect
# Import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.ext.automap import automap_base
# Import data collection needs
import sqlite3 as sql
import pandas as pd
from historical_api import historical_api_call
from historical_api import shortinterval_api_call
# binance
from binance.client import Client
#import config
# Other libraries
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# pip install APScheduler 
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import websocket, json
# from live_update import dict_cryptoinfon


# Set binance connection
client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"))

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
    return render_template ("index.html")
  
# API route
@app.route("/api")
# Return static HTML file with JS code
# Ideally would serve from independent web server, but not practical in test environment
def api():
    return render_template ("test.html")


@app.route("/api/sumtrades")
def sumtrades():
    session = Session(bind=engine)
    execute_string = "select crypto, sum(trade) from historical group by crypto order by sum(trade) desc"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    # Define colours to use
    colours = ({
        "ada_gbp": 'rgba(51, 51, 51, 0.8)',
        "bitcoin_gbp": 'rgba(242, 169, 0, 0.8)',
        "ethereum_gbp": 'rgba(113, 107, 148, 0.8)',
        "ripple_gbp": 'rgba(0, 96, 151, 0.8)',
        "solana_gbp": 'rgba(0, 255, 163, 0.8)'
        })
    handles = ({
        "ada_gbp": "Ada",
        "bitcoin_gbp": "Bitcoin",
        "ethereum_gbp": "Ethereum",
        "ripple_gbp": "Ripple",
        "solana_gbp": "Solana"
    })
    # Form dictionary to return
    coin_dict = {}
    coinorder = 0
    for row in coins:
         coin_dict[coinorder] = ({
         "coin": row[0],
         "sum": row[1],
         "color": colours[row[0]],
         "name": handles[row[0]]
         })
         coinorder += 1
    
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))    

# API call to return volume and trades for all coins
@app.route("/api/linechart")
def line():
    session = Session(bind=engine)
    execute_string = "select * from historical"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    coin_dict = {}
    for row in coins:
        coin_dict[row[0]] = ({
            "crypto": row[1],
            "time": row[2],
            "volume": row[7],
            "trade": row[8]
            })
    
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))


# API call to return all data for one coin
@app.route("/api/historical/<coin>")
def historicaldata(coin):
    session = Session(bind=engine)
    execute_string = "select * from historical where crypto='" + coin + "'"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    coin_dict = {}
    for row in coins:
        coin_dict[row[0]] = ({
            "crypto": row[1], 
            "time": row[2],
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
@app.route("/api/shortinterval/<coin>")
def shortintervaldata(coin):
    session = Session(bind=engine)
    execute_string = "select * from shortinterval where crypto='" + coin + "'"
    coins = engine.execute(execute_string).fetchall()
    session.close()
    
    coin_dict = {}
    for row in coins:
        coin_dict[row[0]] = ({
            "crypto": row[1], 
            "time": row[2],
            "open": row[3],
            "high": row[4],
            "low": row[5],
            "close": row[6],
            "volume": row[7],
            "number_trades": row[8]
            })
    
    # Return dictionary as a JSON file for JS processing
    return(jsonify(coin_dict))

# Fetch live data from live_update.py
# @app.route("/update_livedata/<coin>")
def update_livedata():
    print("start")

    kline_info = {
            "bitcoin_gbp" : 'btcgbp',
            "ethereum_gbp" : 'ethgbp',
            "ada_gbp" : 'adagbp',
            "ripple_gbp" : 'xrpgbp',
            "solana_gbp" :'solgbp'}

    # create dictionary containing info for each coin
    dict_cryptoinfo = {}

    for crypto in kline_info:
        dict_cryptoinfo.update({kline_info[crypto]: 
                [{
                    "time": "",
                    "symbol": "",
                    "open": "",
                    "high": "",
                    "low": "",
                    "close": ""}]})

    socket = f"wss://stream.binance.com:9443/ws/"
    interval = "1m"
    api_call = ""

    # create api call 
    for crypto in kline_info:
        api_info = f"{kline_info[crypto]}@kline_{interval}/"
        api_call += api_info
    api_request = str(socket+api_call)
    api_request = api_request[:-1]

    print(api_request)

    def on_message(ws, message):

        json_message = json.loads(message)
        candle = json_message['k']

        candlestick_dict = {
                "time": candle['t'],
                "symbol": candle['s'],
                "open": candle['o'],
                "high": candle['h'],
                "low": candle['l'],
                "close": candle['c'],
            }
        print(f"live data updated with {candle['s']}")

        # updates the dictionary for the crypto which has received new data, does not change others
        for crypto in kline_info:
            crypto_upper = str(kline_info[crypto]).upper().strip()
            if crypto_upper == candlestick_dict["symbol"]:
                dict_cryptoinfo.update({kline_info[crypto] : candlestick_dict})

        print(dict_cryptoinfo)
        return(dict_cryptoinfo)


    def on_close(ws):
        print("Connection closed!")

    #create a session to connect with binance websocket server
    ws = websocket.WebSocketApp(api_request, on_message=on_message, on_close=on_close)

    #we have to wait 1 minute to get the first data
    ws.close()

    print("end")

# Historical chart page
@app.route("/historical")
def histchart():
    return render_template ("historical.html")

# Line chart page
@app.route("/line")
def linechart():
    return render_template ("line.html")

# Line chart page
@app.route("/bar")
def trades():
    return render_template ("sum-trades.html")

# Live chart page
@app.route("/live")
@app.route("/live/<coin>")
def livechart(coin="bitcoin_gbp"):
    return render_template ("live_chart2.html")

# prints time as test
# def print_date_time():
#     print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def historical_update():
    historical_df = historical_api_call()
    historical_df.to_sql('historical', con=engine, if_exists='replace')
    print("historical_update ran successfully")

def shortinterval_update():
    shortinterval_df = shortinterval_api_call()
    shortinterval_df.to_sql('shortinterval', con=engine, if_exists='replace')
    print("shortinterval_update ran successfully")

#run functions on app startup
# historical_update()
# shortinterval_update()

#run functions every minute/hour
scheduler = BackgroundScheduler()
#scheduler.add_job(func=print_date_time, trigger="interval", seconds=60)
scheduler.add_job(func=shortinterval_update, trigger="interval", seconds=60)
scheduler.add_job(func=historical_update, trigger="interval", seconds=600)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Start Flask app
if __name__ == '__main__':
    app.run()
    now = datetime.now(tz=None).timestamp()
    print(now)

