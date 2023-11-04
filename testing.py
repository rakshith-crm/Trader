from trader.stock import *

ticker_codes = [
    "YESBANK.NS",
    "ITC.NS",
    "NESTLEIND.NS",
    "HINDUNILVR.NS",
    "BRITANNIA.NS",
    "GODREJCP.NS",
    "DABUR.NS",
    "MARICO.NS",
    "UBL.NS",
    "TATACONSUM.NS",
    "ATFL.NS",
    "TATASTEEL.NS",
    "AAPL",
    "BTC-USD",
    "ADANIPORTS.NS",
    "SBIN.NS",
    "SUZLON.NS",
    "IDEA.NS",
    "RELIANCE.NS",
    "HCC.NS",
    "IOC.NS",
    "TATAPOWER.NS",
    "M&M.NS",
]

"""
"""

# for ticker in ticker_codes:
#     print(f"Processing ticker: {ticker}")
#     stock = Stock(ticker)
#     stock.process_data(show_simulation=False, verbose=False)
#     stock.plotter(save_path=f"plots/{ticker}")
#     stock.save_model(save_path=f"models/{ticker}")

# Save model
ticker = ticker_codes[0]
stock = Stock(ticker, disable_stats=True)
stock.process_data(show_simulation=False, verbose=False)
stock.plotter(save_dir=f"plots/")
stock.save_model(save_dir=f"models/")
stock.print_data_shapes()

# Load model
# ticker = ticker_codes[0]
# stock = Stock(ticker)
# stock.load_model(f"models/")
# stock.process_data(show_simulation=False, verbose=False)
# stock.plotter(save_path=f"plots/{ticker}")
# stock.print_data_shapes()
