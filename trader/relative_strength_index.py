import numpy as np
import pandas as pd


def calculate_rsi(stock_price, window_size=14):
    returns = np.diff(stock_price[-window_size - 1: -1])
    net_gains = returns[returns > 0]
    net_losses = returns[returns <= 0]
    avg_gains = np.mean(net_gains)
    avg_losses = abs(np.mean(net_losses))
    rs = avg_gains / avg_losses
    rsi_value = 100 - (100 / (1 + rs))
    rsi_value = pd.Series(data=[rsi_value], index=[stock_price.index[-1]])
    return rsi_value
