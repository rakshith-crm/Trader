import numpy as np
import pandas as pd

from .processor import Queable
from .utils import *

def calculate_rsi(stock_price, window_size=14):
    segment = stock_price[-window_size - 1 : -1]
    returns = np.diff(segment)
    net_gains = returns[returns > 0]
    net_losses = returns[returns <= 0]
    avg_gains = np.mean(net_gains)
    avg_losses = abs(np.mean(net_losses))
    rs = avg_gains / avg_losses
    rsi_value = 100 - (100 / (1 + rs))

    rsi_value = pd.Series(data=[rsi_value], index=[stock_price.index[-1]])
    return rsi_value


class RSI(Queable):
    def __init__(self, stock, window_size) -> None:
        self.stock = stock
        self.processed_till = 0
        self.window_size = window_size
        self.rsi_values = [50 for i in range(self.window_size)]
    
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
            rsi = self.__calculate_rsi(segment)
            self.rsi_values.append(rsi)

        self.processed_till = len(data)

    def result(self):
        return self.rsi_values

    def params(self):
        pass

    def __calculate_rsi(self, data):
        returns = np.diff(data)
        net_gains = returns[returns > 0]
        net_losses = returns[returns <= 0]
        avg_gains = np.mean(net_gains)
        avg_losses = abs(np.mean(net_losses))
        rs = avg_gains / avg_losses
        rsi_value = 100 - (100 / (1 + rs))
        return rsi_value

    