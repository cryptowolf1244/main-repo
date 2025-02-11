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
HistoricalCandles_BTCUSDT_5m_{open_time of the first candle(Unix in seconds)}_{open_time of the last candle(Unix in seconds)}.xlsx

Note: 
-----
*The project's folder should have a "data" folder. The candlestick data will be read/saved from/to this folder.
** The sample candlestick datat for BINANCE's BTCUSDT spot market is avalible in data folder. you can have UPDATE=True to update the excel file