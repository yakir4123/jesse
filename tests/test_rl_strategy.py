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


class TestRLStrategy(unittest.TestCase):
    def test_rl_strategy(self):
        # Creating dummy data
        candles = {
            jh.key(exchanges.SANDBOX, 'BTC-USDT'): {
                'exchange': exchanges.SANDBOX,
                'symbol': 'BTC-USDT',
                'candles': range_candles(5 * 20)
            }
        }

        # Defining routes
        routes = [
            {'symbol': 'BTC-USDT', 'timeframe': timeframes.MINUTE_5, 'strategy': 'RLStrategy'}
        ]

        config['env']['exchanges'][exchanges.SANDBOX]['type'] = 'futures'

        # Running backtest_mode
        backtest_mode.run('000', False, {}, exchanges.SANDBOX, routes, [], '2019-04-01', '2019-04-02', candles)

        # Checking results
        # assert ...


        # Checking that strategy was created and launched
        self.assertIsNotNone(router.routes[0].strategy)
        self.assertIsInstance(router.routes[0].strategy, RLStrategy)
        
        # Checking that agent was initialized
        self.assertIsNotNone(router.routes[0].strategy.agent)
        self.assertIsInstance(router.routes[0].strategy.agent, Agent)
        
        # Additional checks may include:
        # - checking agent state
        # - checking that agent can get state from environment
        # - checking that agent can select actions




rl = RLStrategy()
