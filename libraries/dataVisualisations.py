import matplotlib.pyplot as plt
import pandas as pd 
class BinanceDataVisualisation:
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def BinanceDataGenericChart(self):
        self.dataFrame.plot(kind='line',x='Opentime')
        plt.show()

    def BinanceDataOpenCloseLineChart(self):
        self.dataFrame.plot(kind='line',x='Opentime',y=['Open', 'Close'],color='red')
        plt.show()

    def BinanceDataMovingAverageLineChart(self):
        self.dataFrame.plot(kind='line',x='Opentime',y=['7_Day_Moving_Average'],color='red')
        plt.show()