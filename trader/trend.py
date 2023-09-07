from scipy import stats
from enum import Enum


class TREND(Enum):
    UPWARD = 1
    DOWNWARD = -1
    NEUTRAL = 0
    THRESHOLD = 0.01


def analyse_trend(prices, verbose=True):
    slope = stats.linregress(list(range(0, len(prices))), prices).slope
    if verbose:
        print('SLOPE_VALUE: ', slope)
    if slope > TREND.THRESHOLD.value:
        return TREND.UPWARD
    elif slope < -TREND.THRESHOLD.value:
        return TREND.DOWNWARD
    else:
        return TREND.NEUTRAL
