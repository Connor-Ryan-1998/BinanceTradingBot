import api.binanceAPI as bAPI
import calculations.calculationMethods as cM
import libraries.dataVisualisations as dV
import variables
import time
import os

os.environ["LastTradedQuantity"] = "0" 
os.environ["BuyStatus"] = 'True'
os.environ["SellStatus"] = 'False'

def main():
    AutoTrade()
    # while True:
    #     AutoTrade()
    #     time.sleep(2.5)
        
def AutoTrade():
    ## Trading Token to => TODO: make BTCAUD env variable
    binanceBTCAUD = bAPI.BinanceData('BTCAUD', apiKey = os.environ["APIKey"] , secretKey=os.environ["secretKey"])

    ## User Data
    ## Open Close for last month into dataframe
    monthbinanceBTCAUD = binanceBTCAUD.MonthlyData()[['Opentime','Open', 'Close']]

    ## Calculate Moving Average and spot trade values for the day
    monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SMA7DayDataframe()
    monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SpotBuyDataframe()
    monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SpotSellDataframe()
    spotBuyPrice = monthbinanceBTCAUD['SpotBuyForDay'].tail(1)

    ## Live Data
    livePrice = binanceBTCAUD.LiveData()['price']

    os.environ["LastTradedQuantity"] =  str(int(os.environ["LastTradedQuantity"]) + 1)

    #Execute buy order if Current Price is less than Buy and no current orders exists
    # if ((livePrice <= spotBuyPrice) and (binanceBTCAUD.userDataOpenOrders() == [] and os.environ["BuyStatus"])):
    #     print(os.environ["LastTradedQuantity"])
    #     binanceBTCAUD

    if (binanceBTCAUD.userDataOpenOrders() == [] and bool(os.environ["BuyStatus"])):
        print(binanceBTCAUD.userDataSetBuyOrder(buyPrice=livePrice))
        print(os.environ["LastTradedQuantity"])

        os.environ["BuyStatus"] = 'False'
        os.environ["SellStatus"] = 'True'

    #Execute Sell order if current price is equal to 
    if (binanceBTCAUD.userDataOpenOrders() != [] and bool(os.environ["SellStatus"])):
        print(binanceBTCAUD.userDataSetBuyOrder(buyPrice=livePrice))
        print(os.environ["LastTradedQuantity"])
        os.environ["BuyStatus"] = 'True'
        os.environ["SellStatus"] = 'False'
        
    ## Data visualisation
    # dV.BinanceDataVisualisation(monthbinanceBTCAUD).BinanceDataGenericChart()

if __name__ == '__main__':
    main()    

