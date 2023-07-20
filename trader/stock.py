import numpy as np
import pandas as pd
import yfinance as yf
from trader.relative_strength_index import *
from trader.support_and_resistance import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Stock:
    def __init__(self, ticker: str, period: str):
        self.ticker = ticker
        self.levels = []
        self.compute_every = 7
        self.computed_till = 0
        self.level_window = 30
        self.rsi_window = 14
        self.decrease_check = 14
        self.stock_prices = yf.download(ticker, start="2018-01-01")['Close']
        self.rs_indices = pd.Series(data=[50] * self.rsi_window, index=list(self.stock_prices.index[:self.rsi_window]))
        self.working_data = self.stock_prices[:self.computed_till]
        self.fig, self.ax = plt.subplots(2, 1, figsize=(16, 8))
        self.fig.suptitle(self.ticker)
        self.focus_window_size = 300

    def process_data(self):
        while True:
            if self.computed_till % self.compute_every == 0 and self.computed_till >= self.level_window:
                segment = self.working_data[-self.level_window:]
                self.levels = self.levels + get_support_resistance_levels(segment)
                self.levels = filter_levels(self.levels)
            if self.computed_till > self.rsi_window:
                rsi_score = calculate_rsi(self.working_data, window_size=self.rsi_window)
                self.rs_indices = pd.concat([self.rs_indices, rsi_score])
            self.plotter()
            self.working_data = pd.concat(
                [self.working_data, self.stock_prices[self.computed_till: self.computed_till + 1]])
            self.computed_till += 1
            if self.working_data.shape == self.stock_prices.shape:
                break

    def plotter(self):
        if len(self.working_data) == 0 or len(self.rs_indices) == 0:
            return
        price_decreasing = False
        if len(self.working_data) >= self.decrease_check:
            price_decreasing = True if self.working_data[-1] < self.working_data[-self.decrease_check] else False
        below_30 = True if float(self.rs_indices[-1]) <= 30 else False
        above_70 = True if float(self.rs_indices[-1]) >= 70 else False
        price_color = 'red' if price_decreasing else 'blue'
        rsi_color = 'green' if above_70 else ('red' if below_30 else 'blue')
        self.ax[0].plot(self.working_data[-self.focus_window_size:], c=price_color)
        self.ax[1].plot(self.rs_indices[-self.focus_window_size:], c=rsi_color)
        self.ax[1].axhline(70, c='orange', linestyle='--')
        self.ax[1].axhline(30, c='orange', linestyle='--')
        for level in self.levels:
            self.ax[0].axhline(level[1], c='g', linestyle='--')
            # self.ax[0].scatter(level[0], level[1])
        plt.draw()
        plt.pause(0.1)
        self.ax[0].cla()
        self.ax[1].cla()
