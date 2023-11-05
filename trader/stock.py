import matplotlib.pyplot as plt
import json
from datetime import datetime
import pandas as pd
import os

from .rsi import *
from .rsl import *
from .trend import *
from .display import *
from .ma import *
from .utils import *

FIGURE_DIM = (10, 10)
FROM_DATE = "2020-01-01"
FOCUS_WINDOW_SIZE = DAYS["3mo"]
COMPUTE_EVERY = DAYS["2wk"]
DECREASE_CHECK = DAYS["2wk"]
TREND_ANALYSER_DAYS = DAYS["1yr"]
TREND_ANALYSER_EVERY = DAYS["1mo"]
CANDLE_PLOT = True
POSITIVE_COLOR = "green"
NEUTRAL_COLOR = "orange"
NEGATIVE_COLOR = "red"

fundamentals_yf_maps = {
    "Trailing PE": "trailingPE",
    "Forward PE": "forwardPE",
    "Book Value": "bookValue",
    "Price-To-Book": "priceToBook",
    "Trailing EPS": "trailingEps",
    "Forward EPS": "forwardEps",
    "Recommendation Key": "recommendationKey",
    "Number Of Analyst Opinions": "numberOfAnalystOpinions",
    "Total Debt": "totalDebt",
    "Trailing PEG Ratio": "trailingPegRatio",
}

def get_fundamentals(stock_info):
    fundamentals = {}
    for name, key in fundamentals_yf_maps.items():
        if key in stock_info.keys():
            fundamentals[name] = stock_info[key]
        else:
            fundamentals[name] = "NA"
    return fundamentals


class Stock:
    def __init__(self, ticker="", disable_stats=True):
        self.compute_every = COMPUTE_EVERY
        self.decrease_check = DECREASE_CHECK
        self.focus_window_size = FOCUS_WINDOW_SIZE
        self.plot_candles = CANDLE_PLOT
        self.trend_analyser_days = TREND_ANALYSER_DAYS
        self.trend_analyse_every = TREND_ANALYSER_EVERY
        self.fig, self.ax = plt.subplots(2, 1, figsize=FIGURE_DIM)
        self.fig.suptitle(ticker)
        self.ticker = ticker
        self.levels = []
        self.processed_till = 0
        self.rsl_window = 30
        self.rsi_window = 14
        self.ma_window = 14
        self.current_trend = TREND.NEUTRAL
        self.stock_prices = yf.download(ticker, start=FROM_DATE)  # [:-5]
        self.rs_indices = pd.Series(
            data=[50] * self.rsi_window,
            index=list(self.stock_prices.index[: self.rsi_window]),
        )
        self.moving_average = pd.Series(
            data=[0] * (self.ma_window),
            index=list(self.stock_prices.index[: (self.ma_window)]),
            dtype=float,
        )
        self.working_data = self.stock_prices[: self.processed_till]
        self.disable_stats = disable_stats
        if not self.disable_stats:
            self.stock_info = yf.Ticker(ticker).info
            self.fundamentals = get_fundamentals(self.stock_info)
            self.display_manager = DisplayWindow(
                f"STOCK INFO: {ticker}", window_dims=(600, 200)
            )

    def __del__(self):
        plt.close()

    def process_data(self, show_simulation=True, verbose=True):
        while True:
            if self.working_data.shape == self.stock_prices.shape:
                break
            if (
                self.processed_till % self.compute_every == 0
                and self.processed_till >= self.rsl_window
            ):
                segment = self.working_data[-self.rsl_window :]["Close"]
                self.levels = self.levels + get_support_resistance_levels(segment)
                self.levels = filter_levels(
                    self.levels, current_date=segment.index[-1], verbose=verbose
                )
            if self.processed_till >= self.rsi_window:
                rsi_score = calculate_rsi(
                    self.working_data["Close"], window_size=self.rsi_window
                )
                self.rs_indices = pd.concat([self.rs_indices, rsi_score])
            if (
                self.processed_till >= self.trend_analyser_days
                and self.processed_till % self.trend_analyse_every == 0
            ):
                trend_samples = self.working_data["Close"][-self.trend_analyser_days :]
                self.current_trend = analyse_trend(trend_samples, verbose)
            ma = calculate_ma(self.working_data["Close"], self.ma_window)
            if ma is not None:
                self.moving_average = pd.concat([self.moving_average, ma])

            if show_simulation:
                analysis = {"Trend": self.current_trend.name}
                if not self.disable_stats:
                    analysis.update(self.fundamentals)
                    self.display_manager.update(analysis)
                self.plotter()
            self.working_data = pd.concat(
                [
                    self.working_data,
                    self.stock_prices[self.processed_till : self.processed_till + 1],
                ]
            )
            self.processed_till += 1

        if verbose:
            print("[INFO] PROCESSED UNTIL", self.working_data.index[-1])
            print_table(rows=self.levels, headers=["Date", "Price"])

    def plotter(self, save_dir=None):
        if len(self.working_data) == 0 or len(self.rs_indices) == 0:
            return
        below_30 = True if float(self.rs_indices[-1]) <= 30 else False
        above_70 = True if float(self.rs_indices[-1]) >= 70 else False
        price_color = (
            POSITIVE_COLOR
            if self.current_trend == TREND.UPWARD
            else (
                NEGATIVE_COLOR
                if self.current_trend == TREND.DOWNWARD
                else NEUTRAL_COLOR
            )
        )
        rsi_color = (
            POSITIVE_COLOR
            if above_70
            else (NEGATIVE_COLOR if below_30 else NEUTRAL_COLOR)
        )
        working_data = self.working_data[-self.focus_window_size :]
        if self.plot_candles:
            up = working_data[working_data["Close"] >= working_data["Open"]]
            down = working_data[working_data["Close"] < working_data["Open"]]
            width = 0.5
            width2 = 0.05
            # Plotting up prices of stock
            self.ax[0].bar(
                up.index,
                up["Close"] - up["Open"],
                width,
                bottom=up["Open"],
                color=POSITIVE_COLOR,
            )
            self.ax[0].bar(
                up.index,
                up["High"] - up["Close"],
                width2,
                bottom=up["Close"],
                color=POSITIVE_COLOR,
            )
            self.ax[0].bar(
                up.index,
                up["Low"] - up["Open"],
                width2,
                bottom=up["Open"],
                color=POSITIVE_COLOR,
            )
            # Plotting down prices of stock
            self.ax[0].bar(
                down.index,
                down["Close"] - down["Open"],
                width,
                bottom=down["Open"],
                color=NEGATIVE_COLOR,
            )
            self.ax[0].bar(
                down.index,
                down["High"] - down["Open"],
                width2,
                bottom=down["Open"],
                color=NEGATIVE_COLOR,
            )
            self.ax[0].bar(
                down.index,
                down["Low"] - down["Close"],
                width2,
                bottom=down["Close"],
                color=NEGATIVE_COLOR,
            )
        else:
            self.ax[0].plot(working_data["Close"], c=price_color)
        self.ax[0].plot(self.moving_average[-self.focus_window_size :], c="orange")
        minimum = min(working_data["Close"])
        maximum = max(working_data["Close"])
        self.ax[1].plot(self.rs_indices[-self.focus_window_size :], c=rsi_color)
        self.ax[1].axhline(70, c="orange", linestyle="--")
        self.ax[1].axhline(30, c="orange", linestyle="--")
        for level in self.levels:
            if 0.9 * minimum < level[1] < 1.1 * maximum:
                self.ax[0].axhline(level[1], c="g", linestyle="--")
            # self.ax[0].scatter(level[0], level[1])

        if save_dir is None:
            plt.draw()
            plt.pause(0.05)
        else:
            plt.savefig(os.path.join(save_dir, self.ticker + ".png"))
        self.ax[0].cla()
        self.ax[1].cla()

    def save_model(self, save_dir):
        level_date_as_string = []
        for l in self.levels:
            level_date_as_string.append([datetime.strftime(l[0], "%Y-%m-%d"), l[1]])
        rsi_values_list = list(
            zip(
                [datetime.strftime(ele, "%Y-%m-%d") for ele in self.rs_indices.index],
                self.rs_indices.to_list(),
            )
        )
        ma_list = list(
            zip(
                [
                    datetime.strftime(ele, "%Y-%m-%d")
                    for ele in self.moving_average.index
                ],
                self.moving_average.to_list(),
            )
        )
        model = {
            "ticker": self.ticker,
            "process_parameters": {
                "rsl_window_size": self.rsl_window,
                "rsi_window_size": self.rsi_window,
            },
            "levels": level_date_as_string,
            "rsi_indices": rsi_values_list,
            "moving_average": ma_list,
            "processed_till": datetime.strftime(
                self.working_data.index[-1], "%Y-%m-%d"
            ),
            "processed_from": FROM_DATE,
        }
        json_object = json.dumps(model, indent=4)
        with open(os.path.join(save_dir, self.ticker + ".json"), "w") as file:
            file.write(json_object)

    def load_model(self, model_dir):
        def load_levels(json_object):
            timestamp_levels = []
            for level in json_object["levels"]:
                timestamp = pd.to_datetime(level[0])
                timestamp_levels.append([timestamp, level[1]])
            return timestamp_levels

        def load_rs_indices(json_object):
            timestamp_rsi_indices = [[], []]
            for rsi_val in json_object["rsi_indices"]:
                timestamp = pd.to_datetime(rsi_val[0])
                timestamp_rsi_indices[0].append(timestamp)
                timestamp_rsi_indices[1].append(rsi_val[1])
            return pd.Series(
                data=timestamp_rsi_indices[1], index=timestamp_rsi_indices[0]
            )

        def load_moving_average(json_object):
            timestamp_moving_average = [[], []]
            for ma in json_object["moving_average"]:
                timestamp = pd.to_datetime(ma[0])
                timestamp_moving_average[0].append(timestamp)
                timestamp_moving_average[1].append(ma[1])
            return pd.Series(
                data=timestamp_moving_average[1], index=timestamp_moving_average[0]
            )

        def load_params(json_object):
            processed_till = json_object["processed_till"]
            processed_till = pd.to_datetime(processed_till)
            indices = list(self.stock_prices.index)
            processed_till = indices.index(processed_till) + 1
            return (
                json_object["ticker"],
                json_object["process_parameters"]["rsl_window_size"],
                json_object["process_parameters"]["rsi_window_size"],
                processed_till,
            )

        with open(os.path.join(model_dir, self.ticker + ".json")) as file:
            json_object = json.loads(file.read())

        self.levels = load_levels(json_object)
        self.rs_indices = load_rs_indices(json_object)
        self.moving_average = load_moving_average(json_object)
        (
            self.ticker,
            self.rsl_window,
            self.rsi_window,
            self.processed_till,
        ) = load_params(json_object)

        self.working_data = self.stock_prices[: self.processed_till]
        print("[INFO] Model loaded succesfully restored all states")

    def is_model_exists(self, models_dir):
        if os.path.exists(os.path.join(models_dir, f"{self.ticker}.json")):
            return True
        return False

    def print_data_shapes(self):
        print(f"stock.rs_indices.shape: {self.rs_indices.shape}")
        print(f"stock.ma.shape: {self.moving_average.shape}")
        print(f"stock.processed_till: {self.processed_till}")
        print(f"stock.working_data.shape: {self.working_data.shape}")

# class Stock:
#     def __init__(self, ticker) -> None:
#         self.ticker = ticker
#         self.stock_data = yf.download(ticker, start=FROM_DATE)
        
#     def fundamentals(self):
#         def get_fundamentals(stock_info):
#             fundamentals = {}
#             for name, key in fundamentals_yf_maps.items():
#                 if key in stock_info.keys():
#                     fundamentals[name] = stock_info[key]
#                 else:
#                     fundamentals[name] = "NA"
#             return fundamentals
        
#         stock_info = yf.Ticker(self.ticker).info
#         return get_fundamentals(stock_info)
    
#     def get_data(self):
#         return self.stock_data
