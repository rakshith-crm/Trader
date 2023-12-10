import numpy as np
import pandas as pd

from .utils import *
from .queable import Queable


class RSI(Queable):
    def __init__(self, stock, window_size) -> None:
        self.stock = stock
        self.processed_till = 0
        self.window_size = window_size
        self.rsi_values = [50 for i in range(self.window_size)]
        self.trade_quality = None

    def process(self):
        data = self.stock.get_data()

        if len(data) == self.processed_till:
            return
        else:
            print(f"[INFO] processing: count({len(data) - self.processed_till})")

        index = max(self.processed_till, self.window_size)

        for i in range(index, len(data)):
            from_ = i - self.window_size
            to_ = i
            segment = data[from_:to_]["Close"]
            rsi = self.__calculate_rsi(segment)
            self.rsi_values.append(rsi)

        self.processed_till = len(data)

    def result(self):
        return self.stock.get_data().index, self.rsi_values

    def to_json(self):
        stock_index = self.stock.get_data().index
        if len(stock_index) != len(self.rsi_values) or len(stock_index) != len(self.stock.get_data()):
            print('ERROR IN RSI', self.stock.get_ticker())
        params = {
            "ticker": self.stock.get_ticker(),
            "processed_till": self.processed_till,
            "window_size": self.window_size,
        }
        series = []
        for date, price in zip(stock_index, self.rsi_values):
            ts = to_timestamp(date)
            series.append([ts, price])
        values = {"series": series, "trade_quality": self.trade_quality}
        json_model = {}
        json_model.update(params)
        json_model.update(values)
        return json_model

    def load_json(self, json_model):
        self.processed_till = json_model["processed_till"]
        self.window_size = json_model["window_size"]
        self.trade_quality = json_model["trade_quality"]
        series = json_model["series"]
        values = []
        for date, price in series:
            values.append(price)
        self.rsi_values = values

    def type(self):
        return f"RSI-{self.window_size}"

    def description(self):
        return f"RSI: (window_size: {self.window_size}, processed_till: {self.processed_till}, values: {len(self.rsi_values)})"

    def __calculate_rsi(self, data):
        returns = np.diff(data)
        net_gains = returns[returns > 0]
        net_losses = returns[returns <= 0]
        avg_gains = np.mean(net_gains)
        avg_losses = abs(np.mean(net_losses))
        rs = avg_gains / avg_losses
        rsi_value = 100 - (100 / (1 + rs))
        return rsi_value

    def quality(self):
        current_price = self.stock.get_data()["Close"][-1]
        if are_numbers_close(self.rsi_values[-1], current_price):
            self.trade_quality = True
        else:
            self.trade_quality = False
        return self.trade_quality
