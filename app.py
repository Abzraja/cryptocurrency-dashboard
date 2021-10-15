from flask import Flask, render_template, request, flash, redirect, jsonify
import config, csv, datetime
from binance.client import Client
from binance.enums import *

app = Flask(__name__)
client = Client(config.API_KEY, config.API_SECRET, tld='us')


@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/history')
def history():
    btc_candlestick = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "12 Oct, 2021", "15 Oct, 2021")

    btc_candlesticks = []

    for data in btc_candlestick:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        btc_candlesticks.append(candlestick)

    return jsonify(btc_candlesticks)

@app.route('/eth_history')
def eth_history():
    candlesticks = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_15MINUTE, "12 Oct, 2021", "15 Oct, 2021")

    processed_candlesticks = []

    for data in candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        processed_candlesticks.append(candlestick)

    return jsonify(processed_candlesticks)

@app.route('/ada_history')
def ada_history():
    ada_candlesticks = client.get_historical_klines("ADAUSDT", Client.KLINE_INTERVAL_15MINUTE, "12 Oct, 2021", "15 Oct, 2021")

    cardano_candlesticks = []

    for data in ada_candlesticks:
        candlestick = { 
            "time": data[0] / 1000, 
            "open": data[1],
            "high": data[2], 
            "low": data[3], 
            "close": data[4]
        }

        cardano_candlesticks.append(candlestick)

    return jsonify(cardano_candlesticks)

if __name__ == '__main__':
    app.run(debug=True)