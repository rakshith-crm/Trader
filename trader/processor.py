from tqdm import tqdm
import os
import json
from collections import defaultdict

from .ma import MA
from .rsi import RSI
from .rsl import RSL
from .trend import Trend
from .utils import DAYS
from .queable import Queable

queable_registry = {"MA": MA, "RSI": RSI, "RSL": RSL, "TREND": Trend}


class Processor:
    def __init__(self, stock):
        self.queue = []
        self.stock = stock
        self.trade_quality = defaultdict(bool)

    def add(self, queable_obj: Queable):
        self.queue.append(queable_obj)

    def process(self):
        for obj in tqdm(self.queue):
            obj.process()
            self.trade_quality[obj.type()] = obj.quality()

    def result(self):
        results = []
        for obj in self.queue:
            results.append(obj.result())
        return results

    def quality(self):
        return self.trade_quality

    def type(self):
        return "P"

    def description(self) -> str:
        string_value = "Processor Queue\n---------------\n"

        for index, obj in enumerate(self.queue):
            string_value += f"{index + 1}) " + obj.description() + "\n"
        return string_value

    def to_json(self):
        model = {}
        for obj in self.queue:
            model[obj.type()] = obj.to_json()
        stock_json = self.stock.to_json()
        model["stock"] = stock_json
        return model

    def save(self, dir):
        if not os.path.isdir(dir):
            raise Exception(f"Path {dir} is not a valid directory")

        fullpath = os.path.join(dir, self.stock.get_ticker() + ".json")
        print("saving model to", fullpath)
        model = self.to_json()
        json_object = json.dumps(model, indent=4)
        with open(fullpath, "w") as file:
            file.write(json_object)

    @staticmethod
    def default_processor(stock):
        ma_obj = MA(stock=stock, window_size=DAYS["2wk"])
        ma_obj2 = MA(stock=stock, window_size=DAYS["3wk"])
        ma_obj3 = MA(stock=stock, window_size=DAYS["1mo"] + 5)
        rsl_obj = RSL(stock=stock, window_size=DAYS["1mo"])
        rsi_obj = RSI(stock=stock, window_size=DAYS["2wk"])
        trend_obj14 = Trend(stock=stock, window_size=DAYS["2wk"])
        trend_obj30 = Trend(stock=stock, window_size=DAYS["1mo"])
        trend_obj90 = Trend(stock=stock, window_size=DAYS["3mo"])

        processor = Processor(stock=stock)
        processor.add(ma_obj)
        processor.add(ma_obj2)
        processor.add(ma_obj3)
        processor.add(rsi_obj)
        processor.add(rsl_obj)
        processor.add(trend_obj14)
        processor.add(trend_obj30)
        processor.add(trend_obj90)

        return processor

    @staticmethod
    def load_processor(stock, dir):
        ticker = stock.get_ticker()
        fullpath = os.path.join(dir, stock.get_ticker() + ".json")
        if not os.path.exists(fullpath):
            raise Exception(f"model file {fullpath} does not exist")

        with open(fullpath, "r") as file:
            model = json.load(file)

        processor = Processor(stock=stock)
        for obj_key in model.keys():
            if obj_key == "stock":
                continue
            qobj_type, window_size = obj_key.split("-")
            window_size = int(window_size)
            obj = queable_registry[qobj_type](stock, window_size)
            obj.load_json(model[obj_key])
            print("Loading", obj.description())
            processor.add(obj)

        return processor
