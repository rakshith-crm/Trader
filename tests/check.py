import json
import os
from trader import Stock
MODEL_DIR = 'models/'

for model in os.listdir(MODEL_DIR):
    ticker = model.replace('.json', '')
    stock = Stock(ticker=ticker)
    path = os.path.join(MODEL_DIR, model)
    with open(path, 'r') as file:
        json_model = json.load(file)
        n1 = len(json_model['MA-14']['index'])
        n2 = len(json_model['MA-14']['values'])
        n3 = len(stock.get_data())
        print(ticker, n1, n2, n3)
        if (n1 != n2) or (n1 != n3) or (n2 != n3):
            print('ERROR', json_model['MA-14']['index'][-1], stock.get_data().index[-1])