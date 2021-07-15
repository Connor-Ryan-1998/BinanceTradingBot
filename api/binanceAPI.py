# Imports
import pandas as pd
from datetime import datetime, date, timedelta
import time, hmac, requests, hashlib, json, urllib.parse, logging


class BinanceData():
    #region Constructor
    def __init__(self, symbol, interval = '1d', startTime = date.today() - timedelta(30), url = 'https://api.binance.com/api/v3/', apiKey = '', secretKey = ''):
        self.symbol = symbol
        self.interval = interval
        ## Convert supplied date from format => year-month-day to timestamp
        self.startTime = int(datetime.strptime(str(startTime), '%Y-%m-%d').timestamp() * 1000)
        self.url = url
        self.apiKey = apiKey
        self.secretKey = secretKey

    def __repr__(self):
        return f"BinanceData({self.symbol!r}, {self.interval!r})"

    def __str__(self):
        return f"BinanceData: {self.symbol} {self.interval}"
    #endregion
    #region User Data
    def userDataAccount(self):
        servertime = requests.get("https://api.binance.com/api/v1/time")
        servertimeobject = json.loads(servertime.text)
        servertimeint = servertimeobject['serverTime']

        params = urllib.parse.urlencode({
            "timestamp" : servertimeint,
        })

        hashedsig = hmac.new(self.secretKey.encode('utf-8'), params.encode('utf-8'), 
        hashlib.sha256).hexdigest()

        response = requests.get(self.url + "account",
            params = {
                "timestamp" : servertimeint,
                "signature" : hashedsig,      
            },
            headers = {
                "X-MBX-APIKEY" : self.apiKey,
            }
        )
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return "Failed to retrieve Account Data: " + str(response.status_code) 

    def userDataOpenOrders(self):
        servertime = requests.get("https://api.binance.com/api/v1/time")
        servertimeobject = json.loads(servertime.text)
        servertimeint = servertimeobject['serverTime']

        params = urllib.parse.urlencode({
            "timestamp" : servertimeint,
        })

        hashedsig = hmac.new(self.secretKey.encode('utf-8'), params.encode('utf-8'), 
        hashlib.sha256).hexdigest()

        response = requests.get(self.url + "openOrders",
            params = {
                "timestamp" : servertimeint,
                "signature" : hashedsig,      
            },
            headers = {
                "X-MBX-APIKEY" : self.apiKey,
            }
        )
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return "Failed to retrieve Order Data Data: " + str(response.status_code)
    #endregion
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
    def userDataSetBuyOrder(self, buyPrice):
        servertime = requests.get("https://api.binance.com/api/v1/time")
        servertimeobject = json.loads(servertime.text)
        servertimeint = servertimeobject['serverTime']

        params = {
                "symbol"    : self.symbol,
                "side"      : "BUY",
                "type"      : "MARKET",
                "quoteOrderQty"     : "300",   
            }
        query_string = urllib.parse.urlencode(params, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, servertimeint)
        else:
            query_string = 'timestamp={}'.format(servertimeint)
        hashedsig = hmac.new(self.secretKey.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = self.url  + "order/test" + '?' + query_string + '&signature=' + hashedsig

        params = {'url': url, 'params': {}}
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.apiKey
        })
        response = session.post(**params)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return "Failed to Execute Buy Order: " + str(response.status_code) + " => " + str(response.content)  

    def userDataSetSellOrder(self, sellPrice):     
        servertime = requests.get("https://api.binance.com/api/v1/time")
        servertimeobject = json.loads(servertime.text)
        servertimeint = servertimeobject['serverTime']

        params = {
                "symbol"    : self.symbol,
                "side"      : "SELL",
                "type"      : "MARKET",
                "quoteOrderQty"     : "300"
                # "type"      : "LIMIT",
                # "quoteOrderQty"     : "300",  
            }
        query_string = urllib.parse.urlencode(params, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, servertimeint)
        else:
            query_string = 'timestamp={}'.format(servertimeint)
        hashedsig = hmac.new(self.secretKey.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        url = self.url  + "order/test" + '?' + query_string + '&signature=' + hashedsig

        params = {'url': url, 'params': {}}
        session = requests.Session()
        session.headers.update({
            'Content-Type': 'application/json;charset=utf-8',
            'X-MBX-APIKEY': self.apiKey
        })
        response = session.post(**params)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return "Failed to Execute Buy Order: " + str(response.status_code) + " => " + str(response.content)     
    #endregion
