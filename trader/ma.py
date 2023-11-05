import numpy as np
import pandas as pd

from .processor import *
from .utils import *

def calculate_ma(stock_price, window_size=14):
    if len(stock_price) < window_size:
        return None
    ma = np.mean(stock_price[-window_size:])
    return pd.Series(data=[ma], index=[stock_price.index[-1]])


class MA(Queable):
    def __init__(self, stock, window_size=DAYS["2wk"]) -> None:
        self.stock = stock
        self.processed_till = 0
        self.window_size = window_size
        self.ma_values = [0 for i in range(self.window_size)]
    
    def process(self):
        data = self.stock.get_data()
        
        if len(data) == self.processed_till:
            return

        index = max(self.processed_till, self.window_size)
        print(index)
        for i in range(index, len(data)):
            from_ = i - self.window_size
            to_ = i
            segment = data[from_: to_]["Close"]
            ma = self.__calculate_ma(segment)
            self.ma_values.append(ma)

        self.processed_till = len(data)

    def result(self):
        return self.ma_values

    def params(self):
        pass

    def __calculate_ma(self, data):
        if len(data) < self.window_size:
            return None
        ma = np.mean(data)
        return ma

    