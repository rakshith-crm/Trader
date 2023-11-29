from scipy import stats
from enum import Enum
import numpy as np
from .queable import Queable


class TREND(float, Enum):
    UPWARD = 1
    DOWNWARD = -1
    NEUTRAL = 0
    THRESHOLD = 0.95


class Trend(Queable):
    def __init__(self, stock, window_size):
        self.stock = stock
        self.window_size = window_size
        self.trend = None
        self.trade_quality = None
        self.processed_till = None

    def process(self):
        sliced_prices = self.stock.get_data()[-self.window_size :]["Close"]
        self.trend = self.__analyse_trend(sliced_prices)

        if self.trend == TREND.UPWARD:
            self.trade_quality = True
        else:
            self.trade_quality = False

    def result(self):
        return self.trend

    def to_json(self):
        params = {
            "ticker": self.stock.get_ticker(),
            "processed_till": None,
            "window_size": self.window_size,
        }
        values = {"trend": self.trend, "trade_quality": self.trade_quality}
        json_model = {}
        json_model.update(params)
        json_model.update(values)
        return json_model

    def load_json(self, json_model):
        self.window_size = json_model["window_size"]
        self.processed_till = json_model["processed_till"]
        self.trend = json_model["trend"]
        self.trade_quality = json_model["trade_quality"]

    def type(self):
        return f"TREND-{self.window_size}"

    def description(self):
        return f"Trend: (window_size: {self.window_size})"

    def quality(self):
        return self.trade_quality

    def __analyse_trend(self, prices, verbose=False):
        x = np.arange(0, len(prices)) / len(prices)
        y = np.array(prices)
        y = (y - np.max(y)) / (np.max(y) - np.min(y))
        slope = stats.linregress(x, y).slope
        if verbose:
            print("SLOPE_VALUE: ", slope)
        if slope > TREND.THRESHOLD.value:
            return TREND.UPWARD
        elif slope < -TREND.THRESHOLD.value:
            return TREND.DOWNWARD
        else:
            return TREND.NEUTRAL
