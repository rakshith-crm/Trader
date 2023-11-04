import numpy as np
import pandas as pd


def calculate_ma(stock_price, window_size=14):
    if len(stock_price) < window_size:
        return None
    ma = np.mean(stock_price[-window_size:])
    return pd.Series(data=[ma], index=[stock_price.index[-1]])
