import yfinance as yf
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


class Stock:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.stock_data = yf.download(ticker, start=FROM_DATE)

    def fundamentals(self):
        def get_fundamentals(stock_information):
            fundamentals = {}
            for name, key in fundamentals_yf_maps.items():
                if key in stock_information.keys():
                    fundamentals[name] = stock_information[key]
                else:
                    fundamentals[name] = "NA"
            return fundamentals

        stock_info = yf.Ticker(self.ticker).info
        return get_fundamentals(stock_info)

    def get_data(self):
        return self.stock_data

    def get_ticker(self):
        return self.ticker

    def to_json(self):
        open = self.stock_data["Open"]
        high = self.stock_data["High"]
        low = self.stock_data["Low"]
        close = self.stock_data["Close"]
        values = list(zip(open, high, low, close))
        series = []
        for date, value in zip(self.stock_data.index, values):
            ts = to_timestamp(date)
            series.append([ts, value])
        return {"ticker": self.ticker, "series": series}

    def load_json(self):
        pass

