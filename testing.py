from trader.stock import *

ticker_codes = ['ITC.NS', 'NESTLEIND.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'GODREJCP.NS', 'DABUR.NS', 'MARICO.NS',
                'UBL.NS', 'TATACONSUM.NS', 'ATFL.NS', 'TATASTEEL.NS', 'AAPL', 'BTC-USD', 'ADANIPORTS.NS', 'SBIN.NS',
                'SUZLON.NS', 'IDEA.NS', 'RELIANCE.NS', 'HCC.NS', 'IOC.NS', 'TATAPOWER.NS']

ticker = ticker_codes[-3]

stock = Stock(ticker)
stock.process_data(show_simulation=True, verbose=False)
stock.plotter(save_path=f'plots/{ticker}.png')