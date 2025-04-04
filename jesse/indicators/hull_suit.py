from collections import namedtuple

from .wma import wma
from .ema import ema
import numpy as np
from jesse.helpers import get_candle_source, slice_candles

HullSuit = namedtuple('HullSuit', ['s_hull', 'm_hull', 'signal'])


def hull_suit(candles: np.ndarray, mode_switch: str = 'Hma', length: int = 55, length_mult: float = 1.0, source_type: str = 'close', sequential: bool = False) -> HullSuit:
    """
    @author InSilico
    credits: https://www.tradingview.com/script/hg92pFwS-Hull-Suite/

    HullSuit - Hull Suit

    :param candles: np.ndarray
    :param mode_switch: str - default: 'Hma'
    :param length: int - default: 55
    :param length_mult: float - default: 1.0
    :param source_type: str - default: "closes"
    :param sequential: bool - default=False

    :return: float | np.ndarray
    """
    if len(candles.shape) == 1:
        source = candles
    else:
        candles = slice_candles(candles, sequential)
        source = get_candle_source(candles, source_type=source_type)

    mode_len = int(length * length_mult)
    if mode_switch == 'Hma':
        mode = wma(2*wma(source, int(mode_len / 2), sequential=True) - wma(source, mode_len, sequential=True), round(mode_len ** 0.5), sequential=True)
    elif mode_switch == 'Ehma':
        mode = ema(2*ema(source, int(mode_len / 2), sequential=True) - ema(source,
                   mode_len, sequential=True), round(mode_len ** 0.5), sequential=True)
    elif mode_switch == 'Thma':
        mode = wma(3*wma(source, int(mode_len / 6), sequential=True) - wma(source, int(mode_len / 4), sequential=True) -
                   wma(source, int(mode_len / 2), sequential=True), int(mode_len / 2), sequential=True)

    # Vectorized computation for s_hull, m_hull, and signal
    n = len(mode)
    s_hull = np.full(n, None, dtype=object)
    m_hull = np.full(n, None, dtype=object)
    signal = np.full(n, None, dtype=object)
    if n > 2:
        s_hull[2:] = mode[:-2]
        m_hull[2:] = mode[2:]
        signal[2:] = np.where(mode[:-2] < mode[2:], 'buy', 'sell')

    if sequential:
        return HullSuit(s_hull, m_hull, signal)
    else:
        return HullSuit(s_hull[-1], m_hull[-1], signal[-1])
