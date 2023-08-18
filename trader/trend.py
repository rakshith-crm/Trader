from scipy import stats
from enum import Enum


class TREND(Enum):
    UPWARD = 1
    DOWNWARD = -1
    NEUTRAL = 0
    THRESHOLD = 0.1


def analyse_trend(prices):
    slope = stats.linregress(list(range(0, len(prices))), prices).slope
    print('SLOPE_VALUE: ', slope)
    if slope > TREND.THRESHOLD.value:
        return TREND.UPWARD
    elif slope < -TREND.THRESHOLD.value:
        return TREND.DOWNWARD
    else:
        return TREND.NEUTRAL
