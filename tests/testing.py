from trader import *
import os

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

MODEL_DIR = "models/"
PLOTS_DIR = "plots/"


def process_ticker(ticker):
    print("-" * 150)

    stock = Stock(ticker)
    print("Processing stock ticker", ticker, "number of datapoints", len(stock.get_data()))
    processor = Processor.default_processor(stock=stock)
    # processor = Processor.load_processor(stock=stock, dir=MODEL_DIR)
    processor.process()
    results = processor.result()
    trade_quality = processor.quality()
    print(processor.description())
    processor.save(dir=MODEL_DIR)
    # print("TRADE QUALITIES")
    # for key, value in trade_quality.items():
    #     print(f"| %-10s | %-10s |" % (key, value))
    plotter = Plotter(layout=(2, 1), row_heights=[0.8, 0.2])
    index = stock.get_data().index
    plotter.addCandlestick(stock=stock, row=1, col=1, name=f"Stock {ticker}")
    plotter.addLine(*results[0], row=1, col=1, name="MA14")
    plotter.addLine(*results[1], row=1, col=1, name="MA21")
    plotter.addLine(*results[2], row=1, col=1, name="MA35")
    plotter.addLine(*results[3], row=2, col=1, name="RSI")
    plotter.addHorizontalLine(index, 30, row=2, col=1, name="RSI Lower")
    plotter.addHorizontalLine(index, 70, row=2, col=1, name="RSI Upper")

    for i, level in enumerate(results[4]):
        plotter.addHorizontalLine(
            index=index, y_value=level, row=1, col=1, name=f"Level {i}"
        )

    plotter.save(os.path.join(PLOTS_DIR, ticker))
    print("-" * 150)


# ticker = "UBL.NS"
# process_ticker(ticker=ticker)

for ticker in ticker_codes:
    process_ticker(ticker=ticker)
