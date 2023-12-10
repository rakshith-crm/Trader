import numpy as np
from pytz import utc

from .queable import Queable
from .stock import Stock
from .utils import DAYS, are_numbers_close, to_datetime, to_timestamp


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
            print(f"[INFO] processing: count({len(data) - self.processed_till})")

        index = max(self.processed_till, self.window_size)

        for i in range(index, len(data)):
            from_ = i - self.window_size
            to_ = i
            segment = data[from_:to_]["Close"]
            ma = self.__calculate_ma(segment)
            self.ma_values.append(ma)

        self.processed_till = len(data)

    def result(self):
        return self.stock.get_data().index, self.ma_values

    def to_json(self):
        stock_index = self.stock.get_data().index
        if len(stock_index) != len(self.ma_values) or len(stock_index) != len(self.stock.get_data()):
            print('ERROR IN MA', self.stock.get_ticker())
        params = {
            "ticker": self.stock.get_ticker(),
            "processed_till": self.processed_till,
            "window_size": self.window_size,
        }
        series = []
        for date, price in zip(stock_index, self.ma_values):
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
        self.ma_values = values

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
        current_price = self.stock.get_data()["Close"][-1]
        if are_numbers_close(current_price, self.ma_values[-1]):
            self.trade_quality = True
        else:
            self.trade_quality = False
        return self.trade_quality
