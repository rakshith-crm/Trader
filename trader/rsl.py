import warnings

import numpy as np
import yfinance as yf
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from trader.utils import *
from trader.processor import Queable

warnings.simplefilter(action="ignore", category=FutureWarning)

THRESHOLD = 0.0001


def get_support_resistance_levels(stock_data):
    dataset = list(zip(list(range(0, len(stock_data))), list(stock_data)))
    max_cluster_count = 10
    models = []
    scores = []
    for i in range(2, max_cluster_count + 1):
        kmeans = KMeans(n_clusters=i)
        model = kmeans.fit(dataset)
        labels = model.labels_
        silhouette_value = silhouette_score(dataset, labels)
        models.append(model)
        scores.append(silhouette_value)
    best_model = [model for score, model in sorted(zip(scores, models), reverse=True)][
        0
    ]
    levels = list(sorted(best_model.cluster_centers_, key=lambda x: x[0]))
    levels_dated = []
    for i in range(len(levels)):
        levels_dated.append([stock_data.index[int(levels[i][0])], levels[i][1]])

    return levels_dated


def filter_levels(levels, current_date, remove_old_levels=False, verbose=False):
    no_levels = len(levels)
    price_levels = np.array(levels)[:, 1]
    minimum = np.min(price_levels)
    maximum = np.max(price_levels)
    normalized_levels = list((price_levels - minimum) / (maximum - minimum))

    table_data = [
        [index, level, norm_level]
        for index, level, norm_level in zip(
            range(no_levels), price_levels, normalized_levels
        )
    ]
    if verbose:
        print_table(rows=table_data, headers=["Index", "Levels", "Normalized Levels"])

    remove_indices = set()
    difference_matrix = np.zeros(shape=(no_levels, no_levels))
    for i in range(len(normalized_levels) - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            diff = np.sum((normalized_levels[i] - normalized_levels[j]) ** 2)
            difference_matrix[i][j] = diff
            difference_matrix[j][i] = diff

    indices = np.where(difference_matrix < THRESHOLD)
    new_price_levels = [price_levels[i] for i in range(no_levels)]
    counts = [1 for _ in range(no_levels)]
    for x, y in zip(indices[0], indices[1]):
        if x != y:
            new_price_levels[max(x, y)] += price_levels[min(x, y)]
            counts[max(x, y)] += 1
            remove_indices.add(min(x, y))

    if remove_old_levels:
        for i in range(len(levels)):
            days = (current_date - levels[i][0]).days
            if days >= 200:
                remove_indices.add(i)
    for i in range(no_levels):
        levels[i][1] = new_price_levels[i] // counts[i]
    if verbose:
        print(
            "Removing indices: ",
            remove_indices,
            ", values",
            [price_levels[i] for i in remove_indices],
        )
    return [levels[i] for i in range(len(levels)) if i not in remove_indices]


class RSL(Queable):
    def __init__(self):
        pass

    def process(self):
        pass

    def result(self):
        pass
