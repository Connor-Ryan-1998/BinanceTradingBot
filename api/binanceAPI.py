# Imports
import pandas as pd
from datetime import datetime, date, timedelta
import time

class BinanceData():
    def __init__(self, symbol, interval = '1d', startTime = date.today() - timedelta(30), url = 'https://api.binance.com/api/v3/'):
        self.symbol = symbol
        self.interval = interval
        ## Convert supplied date from format => year-month-day to timestamp
        self.startTime = int(datetime.strptime(str(startTime), '%Y-%m-%d').timestamp() * 1000)
        self.url = url

    def __repr__(self):
        return f"BinanceData({self.symbol!r}, {self.interval!r})"

    def __str__(self):
        return f"BinanceData: {self.symbol} {self.interval}"

    def userData(self):
        url = self.url + 'ticker/price?symbol=' + self.symbol
        df = pd.read_json(url, typ='series')
        df.to_frame()
        return df

    #region Binance Data
    def MonthlyData(self):
        df = pd.DataFrame()
        url = self.url + 'klines?symbol=' + self.symbol + '&interval=' + self.interval + '&startTime=' + str(self.startTime)
        df2 = pd.read_json(url)
        df2.columns = ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime', 'Quote asset volume', 'Number of trades','Taker by base', 'Taker buy quote', 'Ignore']
        df = pd.concat([df2, df], axis=0, ignore_index=True, keys=None) 
        df.reset_index(drop=True, inplace=True)    

        #Replace unix timestamp with UTC datetime
        df['Opentime'] = pd.to_datetime(df['Opentime'], unit='ms')
        df.Opentime = df.Opentime.dt.tz_localize('UTC').dt.tz_convert('Australia/Brisbane')
        return df 

    def LiveData(self):
        url = self.url + 'ticker/price?symbol=' + self.symbol
        df = pd.read_json(url, typ='series')
        df.to_frame()
        return df
    #endregion

    #region Market Orders
    #endregion
    