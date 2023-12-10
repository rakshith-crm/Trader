import warnings
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pandas as pd

from .utils import *
from .queable import Queable

warnings.simplefilter(action="ignore", category=FutureWarning)

THRESHOLD = 0.01


COMPUTE_EVERY = DAYS["2wk"]


class RSL(Queable):
    def __init__(self, stock, window_size=DAYS["1mo"]):
        self.stock = stock
        self.processed_till = 0
        self.period = COMPUTE_EVERY
        self.levels = []
        self.window_size = window_size
        self.trade_quality = None

    def process(self, verbose=False):
        data = self.stock.get_data()
        if self.processed_till == len(data):
            return
        else:
            print(f"[INFO] processing: count({len(data) - self.processed_till})")

        index = (
            max(self.processed_till, self.window_size) // self.period
        ) * self.period + self.period

        for i in range(index, len(data), self.period):
            from_ = i - self.window_size
            to_ = i
            segment = data[from_:to_]["Close"]
            self.levels = self.levels + self.__get_support_resistance_levels(segment)
            self.levels = self.__filter_levels(
                self.levels,
                current_date=segment.index[-1],
                verbose=verbose,
                remove_old_levels=True,
            )

        self.processed_till = len(data)

    def result(self):
        level_values = [l[1] for l in self.levels]
        return level_values

    def to_json(self):
        params = {
            "ticker": self.stock.get_ticker(),
            "processed_till": self.processed_till,
            "period": self.period,
            "window_size": self.window_size,
        }
        levels_string = []
        for date, price in self.levels:
            ts = to_timestamp(date)
            level = [ts, price]
            levels_string.append(level)
        values = {"levels": levels_string, "trade_quality": self.trade_quality}
        json_model = {}
        json_model.update(params)
        json_model.update(values)
        return json_model

    def load_json(self, json_model):
        self.processed_till = json_model["processed_till"]
        self.period = json_model["period"]
        self.window_size = json_model["window_size"]
        self.trade_quality = json_model["trade_quality"]
        price_levels = json_model["levels"]
        levels = []
        for date, price in price_levels:
            level = [to_datetime(date), price]
            levels.append(level)
        self.levels = levels

    def type(self):
        return f"RSL-{self.window_size}"

    def description(self):
        return f"RSL: (window_size: {self.window_size}, processed_till: {self.processed_till}, period: {self.period}, values: {len(self.levels)})"

    def __get_support_resistance_levels(self, stock_data):
        dataset = list(zip(list(range(0, len(stock_data))), list(stock_data)))
        max_cluster_count = 10
        models = []
        scores = []
        for i in range(2, max_cluster_count + 1):
            kmeans = KMeans(n_clusters=i)
            model = kmeans.fit(dataset)
            labels = model.labels_
            silhouette_value = silhouette_score(dataset, labels)
            models.append(model)
            scores.append(silhouette_value)
        best_model = [
            model for score, model in sorted(zip(scores, models), reverse=True)
        ][0]
        levels = list(sorted(best_model.cluster_centers_, key=lambda x: x[0]))
        levels_dated = []
        for i in range(len(levels)):
            levels_dated.append([stock_data.index[int(levels[i][0])], levels[i][1]])

        return levels_dated

    def __filter_levels(
        self, levels, current_date, remove_old_levels=False, verbose=False
    ):
        no_levels = len(levels)
        price_levels = sorted(levels, key=lambda x: x[1])
        index = 0
        while index < (no_levels - 1):
            if are_numbers_close(price_levels[index][1], price_levels[index + 1][1]):
                if price_levels[index + 1][0] > price_levels[index][0]:
                    del price_levels[index]
                else:
                    del price_levels[index + 1]
                no_levels -= 1
            else:
                index += 1
        if remove_old_levels:
            index = 0
            size = len(price_levels)
            while index < size:
                days = (current_date - price_levels[index][0]).days
                if days >= 200:
                    del price_levels[index]
                    size -= 1
                else:
                    index += 1
        return price_levels

    def quality(self):
        current_price = self.stock.get_data()["Close"][-1]
        for date, price in self.levels:
            if are_numbers_close(price, current_price):
                self.trade_quality = True
                return
        self.trade_quality = False
        return self.trade_quality
