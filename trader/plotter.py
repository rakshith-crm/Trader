import yfinance as yf
import plotly.subplots as sp
import plotly.graph_objects as go
import plotly.io as pio

from .stock import Stock
from .utils import DAYS


class Plotter:
    def __init__(self, layout, row_heights=[], focus=DAYS["3mo"]):
        self.fig = sp.make_subplots(
            rows=layout[0], cols=layout[1], row_heights=row_heights, shared_xaxes=True
        )
        self.fig.update_layout(xaxis_rangeslider_visible=False)
        self.focus = focus

    def addLine(self, index, values, row, col, name):
        scatter = go.Scatter(x=index[-self.focus :], y=values[-self.focus :], name=name)
        self.fig.add_trace(scatter, row=row, col=col)

    def addCandlestick(self, index, open, close, high, low, row, col, name):
        candlestick = go.Candlestick(
            x=index[-self.focus :],
            open=open[-self.focus :],
            close=close[-self.focus :],
            high=high[-self.focus :],
            low=low[-self.focus :],
            name=name,
        )
        self.fig.add_trace(candlestick, row=row, col=col)

    def addCandlestick(self, stock: Stock, row, col, name):
        stock_data = stock.get_data()
        candlestick = go.Candlestick(
            x=stock_data.index[-self.focus :],
            open=stock_data.Open[-self.focus :],
            close=stock_data.Close[-self.focus :],
            high=stock_data.High[-self.focus :],
            low=stock_data.Low[-self.focus :],
            name=name,
        )
        self.fig.add_trace(candlestick, row=row, col=col)

    def addHorizontalLine(self, index, y_value, row, col, name):
        y_values = [y_value for i in range(len(index))]
        hline = go.Scatter(x=index[-self.focus :], y=y_values[-self.focus :], name=name)
        self.fig.add_trace(hline, row=row, col=col)

    def save(self, path):
        pio.write_image(self.fig, path + ".png", width=1600, height=1200, scale=3)

    def show(self):
        self.fig.show()
