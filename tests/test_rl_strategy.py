# tests/test_rl_strategy.py
import unittest
from jesse.strategies.RLStrategy import RLStrategy  # Importing RL strategy
from jesse.rl.Agent import Agent
import jesse.helpers as jh
from jesse.enums import timeframes, exchanges
from jesse.factories import range_candles
from jesse.modes import backtest_mode
from jesse.routes import router
from jesse.store import store
from jesse.config import config
from jesse.config import reset_config, set_config
from tests.data import test_candles_1
from jesse.testing_utils import set_up


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


rl = RLStrategy()
