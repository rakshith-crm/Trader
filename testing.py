from trader.stock import *

import matplotlib.pyplot as plt

ticker_codes = ['ITC.NS', 'NESTLEIND.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'GODREJCP.NS', 'DABUR.NS', 'MARICO.NS',
                'UBL.NS', 'TATACONSUM.NS', 'ATFL.NS', 'TATASTEEL.NS', 'AAPL', 'BTC-USD', 'ADANIPORTS.NS', 'SBIN.NS', 'SUZLON.NS', 'IDEA.NS']

ticker = ticker_codes[-1]

stock = Stock(ticker, period='5y')
stock.process_data()