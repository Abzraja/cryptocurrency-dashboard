#pip install websocket-client in terminal

import config
import websocket, json
from binance.client import Client
import pandas as pd

client = Client(config.API_KEY, config.API_SECRET)

# #we can use the following script to get binance API trade pairs
# exchange_info = client.get_exchange_info()
# for s in exchange_info['symbols']:
#     print(s['symbol'])

#define name variables for crypto currencies based on their symbols
bitcoin_gbp = 'btcgbp'
etherium_gbp = 'ethgbp'
ada_gbp = 'adagbp'
binancecoin_usd = 'bnbgbp'
doge_gbp = 'dogegbp'
ripple_gbp = 'xrpgbp'
solana_gbp = 'solgpb'

interval = '1m'

# create websocket client in order to connect to binance websocket server
# we are using kline endpoints for multiple cryptos, see links for more info:
# [https://github.com/binance/binance-spot-api-docs/blob/master/web-socket-streams.md]
# [https://binance-docs.github.io/apidocs/spot/en/#current-average-price]
# for convenience, herebelow just added the streamed data nomenclatures:
# {
#   "e": "kline",     // Event type
#   "E": 123456789,   // Event time
#   "s": "BNBBTC",    // Symbol
#   "k": {
#     "t": 123400000, // Kline start time
#     "T": 123460000, // Kline close time
#     "s": "BNBBTC",  // Symbol
#     "i": "1m",      // Interval
#     "f": 100,       // First trade ID
#     "L": 200,       // Last trade ID
#     "o": "0.0010",  // Open price
#     "c": "0.0020",  // Close price
#     "h": "0.0025",  // High price
#     "l": "0.0015",  // Low price
#     "v": "1000",    // Base asset volume
#     "n": 100,       // Number of trades
#     "x": false,     // Is this kline closed?
#     "q": "1.0000",  // Quote asset volume
#     "V": "500",     // Taker buy base asset volume
#     "Q": "0.500",   // Taker buy quote asset volume
#     "B": "123456"   // Ignore
#   }
# }

socket = f"wss://stream.binance.com:9443/ws/{bitcoin_gbp}@kline_{interval}/{etherium_gbp}@kline_{interval}/{ada_gbp}@kline_{interval}/{binancecoin_usd}@kline_{interval}/{doge_gbp}@kline_{interval}/{ripple_gbp}@kline_{interval}/{solana_gbp}@kline_{interval}"

#create empty list which will hold the obtained data from binance. This list will be moved to the database
db_list = []


# the following two functions (on_message & on_close) are needed to set up long lived connection with websocket servers
# see link for more info: [https://pypi.org/project/websocket-client/]

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    # print(candle)

    #when returning live stream data using websockets, it is returning the data every second and since we set our time interval to 1 minute
    #we want to append our dictionary only every minute (not every second). To do that, we are inserting if condition that will append the dictionary only 
    #when every kline stream is closed.
    if candle['x'] == True:

        database_dict = {
                        'Kline start time': candle['t'],
                        'Kline close time': candle['T'],
                        'Symbol': candle['s'],
                        'Interval':candle['i'],
                        'Open price':candle['o'],
                        'Close price':candle['c'],
                        'High price':candle['h'],
                        'Low price':candle['l'],
                        'Base asset volume':candle['v'],
                        'Number of trades': candle['n'],
                        'Is this kline closed': candle['x']
                     }

        # print(database_dict.values())

        #appending only the values from database_dict into db_list
        for value in database_dict.values():
            db_list.append(value)
        print(db_list)
    

def on_close(ws):
    print("Connection closed!")

#create a session to connect with binance websocket server
ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)

#we have to wait 1 minute to get the first data
ws.run_forever()




                                             

