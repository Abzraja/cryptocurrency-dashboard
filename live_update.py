import config
import websocket, json
from binance.client import Client

client = Client(config.API_KEY, config.API_SECRET)

kline_info = {
        "bitcoin_gbp" : 'btcgbp',
        "etherium_gbp" : 'ethgbp',
        "ada_gbp" : 'adagbp',
        "ripple_gbp" : 'xrpgbp',
        "solana_gbp" :'solgbp'}

socket = f"wss://stream.binance.com:9443/ws/"
interval = "1m"
api_call = ""

for crypto in kline_info:
    api_info = f"{kline_info[crypto]}@kline_{interval}/"
    api_call += api_info
api_request = str(socket+api_call)

api_request = api_request[:-1]

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
    return(candlestick_dict)


def on_close(ws):
    print("Connection closed!")

#create a session to connect with binance websocket server
ws = websocket.WebSocketApp(api_request, on_message=on_message, on_close=on_close)

#we have to wait 1 minute to get the first data
ws.run_forever()