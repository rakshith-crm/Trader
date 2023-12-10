import json
import os
from trader import Stock
MODEL_DIR = 'models/'


def check_models_are_latest():
    has_error = False
    for model in os.listdir(MODEL_DIR):
        ticker = model.replace('.json', '')
        stock = Stock(ticker=ticker)
        path = os.path.join(MODEL_DIR, model)
        with open(path, 'r') as file:
            json_model = json.load(file)
            n2 = len(json_model['MA-14']['series'])
            n3 = len(stock.get_data())
            print(ticker, n2, n3)
            if n2 != n3:
                print('ERROR', json_model['MA-14']['index'][-1], stock.get_data().index[-1])
                has_error = True
    if not has_error:
        print('MODELS ARE LATEST')


check_models_are_latest()