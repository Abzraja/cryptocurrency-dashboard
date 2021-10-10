import config
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

client = Client(config.API_KEY, config.API_SECRET)

def historical_api_call():

    today = datetime.today() 
    yesterday = (today - timedelta(days=1))
    last_year = yesterday - relativedelta(years=1)
    yesterday = yesterday.strftime("%d %b, %Y")
    last_year = last_year.strftime("%d %b, %Y")

    cryptos = {
        "bitcoin_gbp" : 'btcgbp',
        "etherium_gbp" : 'ethgbp',
        "ada_gbp" : 'adagbp',
        "ripple_gbp" : 'xrpgbp',
        "solana_gbp" :'solgbp'}

    db_dict = {}

    for crypto in cryptos:
        container = []
        coin = (cryptos[crypto]).upper()
        candles = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1DAY, last_year, yesterday)

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
        "close" : [],
        "volume" : [],
        "trade": []
        }
    )

    # loop through each time on for each crypto and append to dataframe
    for crypto in cryptos:
        for time_interval in db_dict[crypto][0]:

            date_col = datetime.fromtimestamp(time_interval[0]/1000.0).strftime('%Y-%m-%d')
            open_col = time_interval[1]
            high_col = time_interval[2]
            low_col = time_interval[3]
            close_col = time_interval[4]
            vol_col = time_interval[5]
            trade_col = time_interval[9]

            new_row = [{"crypto": crypto,
                    "date" : date_col,
                    "open" : open_col,
                    "high" : high_col,
                    "low" : low_col,
                    "close" : close_col,
                    "volume" : vol_col,
                    "trade" : trade_col
                    }]

            candle_df = candle_df.append(new_row,ignore_index=True,sort=False)

    return(candle_df)