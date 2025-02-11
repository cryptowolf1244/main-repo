from http import client
from pickle import FALSE, TRUE
from binance.client import Client
import time
import re
import os
from numpy import true_divide
import pandas as pd
from datetime import datetime
"""

This script gets the candlestick data from binance. If there is no candles for the desired asset
in the "data" fodler, the application will download the data from binance from the start date. to
if the end date. If there is no start date specified, the application will download the data from
the beginning of time and if there is no end date specified, the application will download the 
candles untill the current date.

Constants:
---------
-API_KEY: str: The api key for binance.
-ASSETNAME: str: The name of the asset for downloading the candlestick data.
-TIMEFRAME: str: The timeframe for the candlestick data.
-START_DATE: Start date string in UTC format or timestamp in seconds if no data has been provided,
    the application will download the data from the beginning of time.
-END_DATE: End date string in UTC format or timestamp in milliseconds. if no data has been provided,
    the application will download the data untill the current date. If you want to download the data
    untill the current time, you can also pass "NOW" or "now" to this variable
-SAVELOCATION: str(optional): The location to save the candlestick data.
-UPDATE: bool(optional): If True, the application will update the candlestick data and disregard the

Output:
-------
A csv file with the candlestick data. The file name has the following format:
HistoricalCandles_BTCUSDT_5m_{open_time of the first candle(Unix in seconds)}_{open_time of the last candle(Unix in seconds)}.pkl

Note: 
-----
*The project's folder should have a "data" folder. The candlestick data will be read/saved from/to this folder.

"""

SYMBOL = "BTCUSDT"
TIMEFRAME = "5m"
START_DATE = None
END_DATE =   "now"
UPDATE = True
SAVELOCATION = "./data"

API_KEY = 'gcJLtOs6tZYTOBEyIYY0JZBDagmFMkc5SY5T8R792cCUgBn7YCLfG7pOJZG3J36x '
API_SECRET = 'EYyaqoqRyPxozdDQQmlL7xQiHaqDIxgGAav68UoYAznTAOI6darEG132kavhI3Vh'
client = Client(API_KEY, API_SECRET)

# Defining the interval dictionary
intervals = {
    "12h": client.KLINE_INTERVAL_12HOUR,
    "15m": client.KLINE_INTERVAL_15MINUTE,
    "1D": client.KLINE_INTERVAL_1DAY,
    "1h": client.KLINE_INTERVAL_1HOUR,
    "1M": client.KLINE_INTERVAL_1MONTH,
    "1m": client.KLINE_INTERVAL_1MINUTE,
    "2h": client.KLINE_INTERVAL_2HOUR,
    "30m": client.KLINE_INTERVAL_30MINUTE,
    "3m": client.KLINE_INTERVAL_3MINUTE,
    "4h": client.KLINE_INTERVAL_4HOUR,
    "5m": client.KLINE_INTERVAL_5MINUTE,
    "6h": client.KLINE_INTERVAL_6HOUR,
    "8h": client.KLINE_INTERVAL_8HOUR,
    "1W": client.KLINE_INTERVAL_1WEEK,
}


if UPDATE:
    # The dictionary containing start and end unix times of each file in the data folder
    _dict = {}
    files = os.listdir("./data")
    df = pd.DataFrame()

    for file in files:
        z = re.match(f"HistoricalCandles_{SYMBOL}_{TIMEFRAME}_(\d+)_(\d+).pkl", file)

        if z != None:
            startUnix = z.group(1)
            endUnix   = z.group(2)

            _dict[startUnix] = endUnix
            
            df = pd.concat([df, pd.read_pickle("./data/" + file)])
    
    if len(_dict) != 0:
        # Getting the last candle's timestamp
        startingPoint = int(max(_dict.values())) * 1000
        endingPoint = END_DATE * 1000 if (END_DATE) and (END_DATE != "now") and (END_DATE != "NOW")  else None

        print(f"Updating dataset, Starting from unix time (milliseonds) {startingPoint} untill {endingPoint}")

        kline = client.get_historical_klines(SYMBOL, intervals[TIMEFRAME], start_str = startingPoint, end_str = endingPoint)
        
        print("Candles loaded, appending...")

        candles = pd.DataFrame(kline).astype(str).astype(float)
        candles.columns = columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ohlc4"]
        candles["open_time"] = candles["open_time"]/1000
        candles["open_time"] = candles["open_time"].round(0).astype(int)

        candles["close_time"] = candles["close_time"]/1000
        candles["close_time"] = candles["close_time"].round(0).astype(int)
        candles = pd.concat([df, candles.iloc[1:]])
        
        # Processign the data
        candles = candles.drop(columns=["ohlc4"])

        candles.to_pickle(f"./data/HistoricalCandles_{SYMBOL}_{TIMEFRAME}_{int(candles.iloc[0,0])}_{int(candles.iloc[-1,0])}.pkl")

        print(f"Updating completed. \n Saved to: HistoricalCandles_{SYMBOL}_{TIMEFRAME}_{int(candles.iloc[0,0])}_{int(candles.iloc[-1,0])}.xlsx")
    else:
        print("Candlestick data not found; check the entries.")


else:
    kline = client.get_historical_klines(SYMBOL, intervals[TIMEFRAME], start_str= START_DATE * 1000)

    candles = pd.DataFrame(kline).astype(str).astype(float)
    candles.columns = columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ohlc4"]
        
    # Processign the data
    candles["open_time"] = candles["open_time"]/1000 # Converting the unix time to datetime
    candles["open_time"] = candles["open_time"].round(0).astype(int)

    candles["close_time"] = candles["close_time"]/1000 # Converting the unix time to datetime
    candles["close_time"] = candles["close_time"].round(0).astype(int)
    candles = candles.drop(columns=["ohlc4"])

    candles.to_pickle(f"./data/HistoricalCandles_{SYMBOL}_{TIMEFRAME}_{candles.iloc[0,0]}_{candles.iloc[-1,0]}.pkl")
    pass
