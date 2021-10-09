import config
from binance.client import Client
import pandas as pd

client = Client(config.API_KEY, config.API_SECRET)

cryptos = {
    "bitcoin_gbp" : 'btcgbp',
    }

db_dict = {}

for crypto in cryptos:
    container = []
    coin = (cryptos[crypto]).upper()
    candles = client.get_historical_klines(coin, Client.KLINE_INTERVAL_15MINUTE, "30 Sep, 2021", "1 Oct, 2021")

    for candlestick in candles:
        container.append(candlestick)
    db_dict[crypto] = [container]

# empty dataframe to hold values
candle_df = pd.DataFrame(
    {"crypto": [],
     "date" : [],
     "open" : [],
     "high" : [],
     "low" : [],
     "close" : []
     }
)

# loop through each time on for each crypto and append to dataframe
for crypto in cryptos:
    for time_interval in db_dict[crypto][0]:

        date_col = time_interval[0]
        open_col = time_interval[1]
        high_col = time_interval[2]
        low_col = time_interval[3]
        close_col = time_interval[4]

        new_row = {"crypto": crypto,
                 "date" : date_col,
                 "open" : open_col,
                 "high" : high_col,
                 "low" : low_col,
                 "close" : close_col
                }
        print(new_row)
        candle_df = candle_df.append(new_row,ignore_index=True,sort=False)

