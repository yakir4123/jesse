# tests/test_rl_strategy.py
import unittest

import jesse.helpers as jh
from jesse.enums import timeframes, exchanges
from jesse.modes import backtest_mode
from jesse.store import store
from jesse.strategies.RLStrategy import RLStrategy  # Importing RL strategy
from jesse.testing_utils import set_up
from tests.data import test_candles_1, test_candles_0


class TestRLStrategy(unittest.TestCase):
    def test_rl_strategy(self):
        set_up()

        routes = [
            {'symbol': 'ETH-USDT', 'timeframe': timeframes.MINUTE_1, 'strategy': 'RLStrategy'}
        ]

        candles = {}
        key = jh.key(exchanges.SANDBOX, 'ETH-USDT')
        candles[key] = {
            'exchange': exchanges.SANDBOX,
            'symbol': 'ETH-USDT',
            'candles': test_candles_1
        }
        backtest_mode.run('000', False, {}, exchanges.SANDBOX, routes, [], '2019-04-01', '2019-04-02', candles)

        assert len(store.completed_trades.trades) > 0

        # Checking results
        # assert ...

        # Checking that strategy was created and launched
        # self.assertIsNotNone(router.routes[0].strategy)
        # self.assertIsInstance(router.routes[0].strategy, RLStrategy)

        # Checking that agent was initialized
        # self.assertIsNotNone(router.routes[0].strategy.agent)
        # self.assertIsInstance(router.routes[0].strategy.agent, Agent)

        # Additional checks may include:
        # - checking agent state
        # - checking that agent can get state from environment
        # - checking that agent can select actions

    def test_rl_strategy_1(self):
        set_up()
        routes = [
            {'symbol': 'BTC-USDT', 'timeframe': timeframes.HOUR_1, 'strategy': 'RLStrategy'}
        ]
        data_routes = [
            # {'symbol': 'BTC-USDT', 'timeframe': timeframes.MINUTE_15}
        ]

        candles = {}
        key = jh.key(exchanges.SANDBOX, 'BTC-USDT')
        candles[key] = {
            'exchange': exchanges.SANDBOX,
            'symbol': 'BTC-USDT',
            'candles': test_candles_0
        }

        backtest_mode.run('000', False, {}, exchanges.SANDBOX, routes, data_routes, '2019-04-01', '2019-04-02', candles)

        assert len(store.completed_trades.trades) > 0



rl = RLStrategy()
