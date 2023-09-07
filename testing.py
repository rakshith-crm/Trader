from trader.stock import *

ticker_codes = ['ITC.NS', 'NESTLEIND.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'GODREJCP.NS', 'DABUR.NS', 'MARICO.NS',
                'UBL.NS', 'TATACONSUM.NS', 'ATFL.NS', 'TATASTEEL.NS', 'AAPL', 'BTC-USD', 'ADANIPORTS.NS', 'SBIN.NS',
                'SUZLON.NS', 'IDEA.NS', 'RELIANCE.NS', 'HCC.NS', 'IOC.NS', 'TATAPOWER.NS', 'M&M.NS']

ticker = ticker_codes[-1]

for ticker in ticker_codes:
    print(f'Processing ticker: {ticker}')
    stock = Stock(ticker)
    stock.process_data(show_simulation=False, verbose=False)
    stock.plotter(save_path=f'plots/{ticker}.png')
