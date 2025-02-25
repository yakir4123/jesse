from collections import namedtuple

import numpy as np

from jesse.helpers import get_candle_source, np_shift, slice_candles

GATOR = namedtuple('GATOR', ['upper', 'lower', 'upper_change', 'lower_change'])


def gatorosc(candles: np.ndarray, source_type: str = "close", sequential: bool = False) -> GATOR:
    """
    Gator Oscillator by Bill M. Williams

    :param candles: np.ndarray
    :param source_type: str - default: "close"
    :param sequential: bool - default: False

    :return: GATOR(upper, lower, upper_change, lower_change)
    """

    candles = slice_candles(candles, sequential)

    source = get_candle_source(candles, source_type=source_type)

    jaw = np_shift(numpy_ewma(source, 13), 8, fill_value=np.nan)
    teeth = np_shift(numpy_ewma(source, 8), 5, fill_value=np.nan)
    lips = np_shift(numpy_ewma(source, 5), 3, fill_value=np.nan)

    upper = np.abs(jaw - teeth)
    lower = -np.abs(teeth - lips)

    # Calculate momentum for upper: difference from previous value, first element is np.nan
    upper_change = np.empty_like(upper)
    upper_change[0] = np.nan
    upper_change[1:] = np.diff(upper)

    # Calculate momentum for lower: negative difference from previous value, first element is np.nan
    lower_change = np.empty_like(lower)
    lower_change[0] = np.nan
    lower_change[1:] = -np.diff(lower)

    if sequential:
        return GATOR(upper, lower, upper_change, lower_change)
    else:
        return GATOR(upper[-1], lower[-1], upper_change[-1], lower_change[-1])


def numpy_ewma(data, window):
    """

    :param data:
    :param window:
    :return:
    """
    alpha = 1 / window
    # scale = 1 / (1 - alpha)
    n = data.shape[0]
    scale_arr = (1 - alpha) ** (-1 * np.arange(n))
    weights = (1 - alpha) ** np.arange(n)
    pw0 = (1 - alpha) ** (n - 1)
    mult = data * pw0 * scale_arr
    cumsums = mult.cumsum()
    return cumsums * scale_arr[::-1] / weights.cumsum()
