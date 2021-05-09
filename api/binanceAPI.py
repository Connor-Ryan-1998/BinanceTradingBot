# Imports
import pandas as pd
from datetime import datetime, date

class BinanceData():
    def __init__(self, symbol, interval = '1d', startTime = date.today().timestamp()):
        self.symbol = symbol
        self.interval = interval
        self.startTime = startTime

    def __repr__(self):
        return f"BinanceData({self.symbol!r}, {self.interval!r})"

    def __str__(self):
        return f"BinanceData: {self.symbol} {self.interval}"

    def monthData(self):
        df = pd.DataFrame()
        url = 'https://api.binance.com/api/v3/klines?symbol=' + self.symbol + '&interval=' + self.interval + '&startTime' + str(self.startTime)
        df2 = pd.read_json(url)
        df2.columns = ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', 'Quote asset volume', 'Number of trades','Taker by base', 'Taker buy quote', 'Ignore']
        df = pd.concat([df2, df], axis=0, ignore_index=True, keys=None) 
        df.reset_index(drop=True, inplace=True)    

        #Replace unix timestamp with UTC datetime
        df['Opentime'] = pd.to_datetime(df['Opentime'], unit='ms')
        df.Opentime = df.Opentime.dt.tz_localize('UTC').dt.tz_convert('Australia/Brisbane')
        return df 

    