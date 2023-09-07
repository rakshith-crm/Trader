import matplotlib.pyplot as plt

from trader.rsi import *
from trader.rsl import *
from trader.trend import *
from trader.display import *

FIGURE_DIM = (14, 8)
FROM_DATE = "2020-01-01"
FOCUS_WINDOW_SIZE = DAYS['3mo']
COMPUTE_EVERY = DAYS['2wk']
DECREASE_CHECK = DAYS['2wk']
TREND_ANALYSER_DAYS = DAYS['1yr']
TREND_ANALYSER_EVERY = DAYS['1mo']
CANDLE_PLOT = True
POSITIVE_COLOR = 'green'
NEUTRAL_COLOR = 'orange'
NEGATIVE_COLOR = 'red'

fundamentals_yf_maps = {'Trailing PE': 'trailingPE',
                        'Forward PE': 'forwardPE',
                        'Book Value': 'bookValue',
                        'Price-To-Book': 'priceToBook',
                        'Trailing EPS': 'trailingEps',
                        'Forward EPS': 'forwardEps',
                        'Recommendation Key': 'recommendationKey',
                        'Number Of Analyst Opinions': 'numberOfAnalystOpinions',
                        'Total Debt': 'totalDebt',
                        'Trailing PEG Ratio': 'trailingPegRatio'}


def get_fundamentals(stock_info):
    fundamentals = {}
    for name, key in fundamentals_yf_maps.items():
        if key in stock_info.keys():
            fundamentals[name] = stock_info[key]
        else:
            fundamentals[name] = 'NA'
    return fundamentals


class Stock:
    def __init__(self, ticker: str):
        self.compute_every = COMPUTE_EVERY
        self.decrease_check = DECREASE_CHECK
        self.focus_window_size = FOCUS_WINDOW_SIZE
        self.plot_candles = CANDLE_PLOT
        self.trend_analyser_days = TREND_ANALYSER_DAYS
        self.trend_analyse_every = TREND_ANALYSER_EVERY
        self.fig, self.ax = plt.subplots(2, 1, figsize=FIGURE_DIM)
        self.fig.suptitle(ticker)
        self.display_manager = DisplayWindow(f'STOCK INFO: {ticker}', window_dims=(600, 200))
        self.ticker = ticker
        self.levels = []
        self.processed_till = 0
        self.rsl_window = 30
        self.rsi_window = 14
        self.current_trend = TREND.NEUTRAL
        self.stock_prices = yf.download(ticker, start=FROM_DATE)
        self.stock_info = yf.Ticker(ticker).info
        self.rs_indices = pd.Series(data=[50] * self.rsi_window, index=list(self.stock_prices.index[:self.rsi_window]))
        self.working_data = self.stock_prices[:self.processed_till]
        self.fundamentals = get_fundamentals(self.stock_info)

    def process_data(self, show_simulation=True, verbose=True):
        while True:
            if self.processed_till % self.compute_every == 0 and self.processed_till >= self.rsl_window:
                segment = self.working_data[-self.rsl_window:]['Close']
                self.levels = self.levels + get_support_resistance_levels(segment)
                self.levels = filter_levels(self.levels, current_date=segment.index[-1], verbose=verbose)
            if self.processed_till > self.rsi_window:
                rsi_score = calculate_rsi(self.working_data['Close'], window_size=self.rsi_window)
                self.rs_indices = pd.concat([self.rs_indices, rsi_score])
            if self.processed_till > self.trend_analyser_days and self.processed_till % self.trend_analyse_every == 0:
                trend_samples = self.working_data['Close'][-self.trend_analyser_days:]
                self.current_trend = analyse_trend(trend_samples, verbose)
            if show_simulation:
                analysis = {'Trend': self.current_trend.name}
                analysis.update(self.fundamentals)
                self.display_manager.update(analysis)
                self.plotter()
            self.working_data = pd.concat(
                [self.working_data, self.stock_prices[self.processed_till: self.processed_till + 1]])
            self.processed_till += 1
            if self.working_data.shape == self.stock_prices.shape:
                break
        if verbose:
            print('[INFO] PROCESSED UNTIL', self.working_data.index[-1])
            print_table(rows=self.levels, headers=['Date', 'Price'])

    def plotter(self, save_path=None, focus=True):
        if len(self.working_data) == 0 or len(self.rs_indices) == 0:
            return
        below_30 = True if float(self.rs_indices[-1]) <= 30 else False
        above_70 = True if float(self.rs_indices[-1]) >= 70 else False
        price_color = POSITIVE_COLOR if self.current_trend == TREND.UPWARD else (
            NEGATIVE_COLOR if self.current_trend == TREND.DOWNWARD else NEUTRAL_COLOR)
        rsi_color = POSITIVE_COLOR if above_70 else (NEGATIVE_COLOR if below_30 else NEUTRAL_COLOR)
        working_data = self.working_data[-self.focus_window_size:]
        if self.plot_candles:
            up = working_data[working_data['Close'] >= working_data['Open']]
            down = working_data[working_data['Close'] < working_data['Open']]
            width = 0.5
            width2 = 0.05
            # Plotting up prices of stock
            self.ax[0].bar(up.index, up['Close'] - up['Open'], width, bottom=up['Open'], color=POSITIVE_COLOR)
            self.ax[0].bar(up.index, up['High'] - up['Close'], width2, bottom=up['Close'], color=POSITIVE_COLOR)
            self.ax[0].bar(up.index, up['Low'] - up['Open'], width2, bottom=up['Open'], color=POSITIVE_COLOR)
            # Plotting down prices of stock
            self.ax[0].bar(down.index, down['Close'] - down['Open'], width, bottom=down['Open'], color=NEGATIVE_COLOR)
            self.ax[0].bar(down.index, down['High'] - down['Open'], width2, bottom=down['Open'], color=NEGATIVE_COLOR)
            self.ax[0].bar(down.index, down['Low'] - down['Close'], width2, bottom=down['Close'], color=NEGATIVE_COLOR)
        else:
            self.ax[0].plot(working_data['Close'], c=price_color)

        minimum = min(working_data['Close'])
        maximum = max(working_data['Close'])
        self.ax[1].plot(self.rs_indices[-self.focus_window_size:], c=rsi_color)
        self.ax[1].axhline(70, c='orange', linestyle='--')
        self.ax[1].axhline(30, c='orange', linestyle='--')
        for level in self.levels:
            if 0.9 * minimum < level[1] < 1.1 * maximum:
                self.ax[0].axhline(level[1], c='g', linestyle='--')
            # self.ax[0].scatter(level[0], level[1])

        if save_path is None:
            plt.draw()
            plt.pause(0.05)
        else:
            plt.savefig(save_path)
        self.ax[0].cla()
        self.ax[1].cla()

    def save_model(self):
        model = {
            'ticker': self.ticker,
            'process_parameters': {
                'rsl_window': self.rsl_window,
                'rsi_window': self.rsi_window
            },
            'levels': self.levels,
            'processed_till': self.working_data.index[-1],
            'processed_from': FROM_DATE
        }
