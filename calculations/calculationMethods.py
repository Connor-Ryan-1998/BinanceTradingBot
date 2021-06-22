import numpy as np
import pandas as pd

class CalculationMethods():
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def __repr__(self):
        return f"CalculationMethods({self.dataFrame!r}"

    def __str__(self):
        return f"CalculationMethods: {self.dataFrame}"


    def SMA7DayDataframe(self):
        self.dataFrame['7_Day_Moving_Average'] = self.dataFrame.iloc[:,1].rolling(window=7).mean()
        return self.dataFrame

    def SpotBuyDataframe(self):
        self.dataFrame['7_Day_Moving_Average'] = self.dataFrame.iloc[:,1].rolling(window=7).mean()
        return self.dataFrame


    def SpotBuyDataframe(self):
        self.dataFrame['SpotBuyForDay'] = self.dataFrame['7_Day_Moving_Average'] * .98
        return self.dataFrame

    def SpotSellDataframe(self):
        self.dataFrame['SpotSellForDay'] = self.dataFrame['7_Day_Moving_Average'] * 1.02
        return self.dataFrame

