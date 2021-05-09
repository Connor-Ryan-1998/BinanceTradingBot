import api.binanceAPI as bAPI
from datetime import datetime as dt
import os

workingData = bAPI.BinanceData('BTCAUD')

print(workingData.monthData()[['Opentime','Low', 'High']])
