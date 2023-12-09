import json
import os
from trader import Stock
MODEL_DIR = 'models2/'


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


def check_models_correctness():
    has_error = False
    model1 = 'models/AAPL.json'
    model2 = 'models2/AAPL.json'
    with open(model1) as file:
        json_model1 = json.load(file)
    with open(model2) as file:
        json_model2 = json.load(file)
    series = json_model2["RSI-14"]["series"]
    values_true = json_model1["RSI-14"]["values"]
    values_check = []
    for price in series:
        values_check.append(price["value"])
    for v1, v2 in zip(values_true, values_check):
        if v1 != v2:
            has_error = True
            print('NOT EQUAL')
    if not has_error:
        print("ALL GOOD")


check_models_correctness()
check_models_are_latest()