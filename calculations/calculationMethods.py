class CalculationMethods():
    def __init__(self, dataFrame):
        self.dataFrame = dataFrame

    def __repr__(self):
        return f"CalculationMethods({self.dataFrame!r}"

    def __str__(self):
        return f"CalculationMethods: {self.dataFrame}"


    def movingAverage(self):
        