import numpy as np

from .queable import Queable
from .stock import Stock
from .utils import *


class MA(Queable):
    def __init__(self, stock: Stock, window_size=DAYS["2wk"]) -> None:
        self.stock = stock
        self.processed_till = 0
        self.window_size = window_size
        self.ma_values = [
            self.stock.get_data()["Close"][0] for _ in range(self.window_size)
        ]
        self.trade_quality = None

    def process(self):
        data = self.stock.get_data()

        if len(data) == self.processed_till:
            return
        else:
            print(f"Processing data: count({len(data) - self.processed_till})")

        index = max(self.processed_till, self.window_size)

        for i in range(index, len(data)):
            from_ = i - self.window_size
            to_ = i
            segment = data[from_:to_]["Close"]
            ma = self.__calculate_ma(segment)
            self.ma_values.append(ma)

        self.processed_till = len(data)

        # Check trade quality
        current_price = self.stock.get_data()["Close"][-1]
        if are_numbers_close(current_price, self.ma_values[-1]):
            self.trade_quality = True
        else:
            self.trade_quality = False

    def result(self):
        return self.stock.get_data().index, self.ma_values

    def to_json(self):
        index = list(self.stock.get_data().index.astype(str))
        if len(index) != len(self.ma_values) or len(index) != len(self.stock.get_data()):
            print('ERROR IN MA', self.stock.get_ticker())
        params = {
            "ticker": self.stock.get_ticker(),
            "processed_till": self.processed_till,
            "window_size": self.window_size,
        }
        values = {"index": index, "values": self.ma_values, "trade_quality": self.trade_quality}
        json_model = {}
        json_model.update(params)
        json_model.update(values)
        return json_model

    def load_json(self, json_model):
        self.processed_till = json_model["processed_till"]
        self.window_size = json_model["window_size"]
        self.ma_values = json_model["values"]
        self.trade_quality = json_model["trade_quality"]

    def type(self):
        return f"MA-{self.window_size}"

    def description(self):
        return f"MA: (window_size: {self.window_size}, processed_till: {self.processed_till}, values: {len(self.ma_values)})"

    def __calculate_ma(self, data):
        if len(data) < self.window_size:
            return None
        ma = np.mean(data)
        return ma

    def quality(self):
        return self.trade_quality
