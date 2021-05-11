import api.binanceAPI as bAPI
import calculations.calculationMethods as cM
import libraries.dataVisualisations as dV
import os

## Trading Token to => TODO: make BTCAUD env variable
binanceBTCAUD = bAPI.BinanceData('BTCAUD')

## User Data
print(binanceBTCAUD.userData())
## Open Close for last month into dataframe
monthbinanceBTCAUD = binanceBTCAUD.MonthlyData()[['Opentime','Open', 'Close']]

## Calculate Moving Average and spot trade values for the day
monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SMA7DayDataframe()
monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SpotBuyDataframe()
monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SpotSellDataframe()

## LiveData
dayBinanceBTCAUD = binanceBTCAUD.LiveData()


## Data visualisation
# dV.BinanceDataVisualisation(monthbinanceBTCAUD).BinanceDataGenericChart()



