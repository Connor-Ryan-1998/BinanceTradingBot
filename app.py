from datetime import datetime
import api.binanceAPI as bAPI
import calculations.calculationMethods as cM
import libraries.dataVisualisations as dV
import variables
import time
import os


def main():
    # AutoTrade()
    os.environ["BuyStatus"] = 'True'
    os.environ["SellStatus"] = 'False'
    while True:
        AutoTrade()
        time.sleep(2.5)
        
def AutoTrade():
    ## Build Token Information
    binanceBTCAUD = bAPI.BinanceData(os.environ["coinToken"] , apiKey = os.environ["APIKey"] , secretKey=os.environ["secretKey"])

    ## User Data
    ## Open Close for last month into dataframe
    monthbinanceBTCAUD = binanceBTCAUD.MonthlyData()[['Opentime','Open', 'Close']]

    ## Calculate Moving Average and spot trade values for the day
    monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SMA7DayDataframe()
    monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SpotBuyDataframe()
    monthbinanceBTCAUD = cM.CalculationMethods(monthbinanceBTCAUD).SpotSellDataframe()
    spotBuyPrice = monthbinanceBTCAUD['SpotBuyForDay'].tail(1)
    SpotSellForDay = monthbinanceBTCAUD['SpotSellForDay'].tail(1)

    ## Live Data
    livePrice = binanceBTCAUD.LiveData()['price']


    #Execute Buy order
    if (float(livePrice) <= float(spotBuyPrice) and binanceBTCAUD.userDataOpenOrders() == [] and os.environ["BuyStatus"] == 'True'):
        output = binanceBTCAUD.userDataSetBuyOrder(buyPrice=300)
        if (output == {}): # Successful trade
            os.environ["BuyStatus"] = 'False'
            os.environ["SellStatus"] = 'True'
            print("Trade Buy Order for " + str(livePrice) + " At " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  +  " Success ")
            return
        else:
            print("Trade Buy Order for " + str(livePrice) + " At " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")+ output[0] +  " Failed ")
            return

    #Execute Sell order 
    if (float(livePrice) >= float(SpotSellForDay) and binanceBTCAUD.userDataOpenOrders() != [] and os.environ["SellStatus"] == 'False'):
        output = binanceBTCAUD.userDataSetSellOrder(sellPrice=307)
        if (output == {}): # Successful trade
            os.environ["BuyStatus"] = 'True'
            os.environ["SellStatus"] = 'False'
            print("Trade Sell Order for " + str(livePrice) + " At " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")  + str(output) +  " Success ")
            return
        else:
            print("Trade Sell Order for " + str(livePrice) + " At " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + output[0] +  " Failed ")
            return
        
    ## Data visualisation
    # dV.BinanceDataVisualisation(monthbinanceBTCAUD).BinanceDataGenericChart()

if __name__ == '__main__':
    main()    

