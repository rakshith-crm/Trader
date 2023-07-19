from trader.support_and_resistance import *
import matplotlib.pyplot as plt

ticker_codes = ['ITC.NS', 'NESTLEIND.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'GODREJCP.NS', 'DABUR.NS', 'MARICO.NS',
                'UBL.NS', 'TATACONSUM.NS', 'ATFL.NS']

ticker = ticker_codes[7]
plt.figure(figsize=(15, 10))

stock_data = get_stock_data(ticker, period='5y')['Close']
segment_size = 30
from_date = 0
to_date = segment_size
levels = []
while True:
    segment = stock_data[from_date:to_date]
    levels = levels + get_support_resistance_levels(segment)
    levels = filter_levels(levels)
    plt.plot(stock_data[:to_date])
    curr_value = segment[-1]
    print(curr_value)
    for level in levels:
        plt.axhline(level[1], c='g', ls='--')
        plt.scatter(level[0], level[1])
    plt.draw()
    plt.pause(5)
    plt.clf()
    from_date += segment_size
    to_date += segment_size
    if to_date >= len(stock_data):
        break
