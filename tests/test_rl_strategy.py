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
from jesse.config import reset_config
from tests.data import test_candles_1



def set_up(is_futures_trading=True, leverage=1, leverage_mode='cross', fee=0):
    reset_config()
    config['env']['exchanges'][exchanges.SANDBOX]['balance'] = 10_000

    config['env']['exchanges']['Sandbox']['fee'] = fee

    if is_futures_trading:
        # used only in futures trading
        config['env']['exchanges'][exchanges.SANDBOX]['type'] = 'futures'
        config['env']['exchanges'][exchanges.SANDBOX]['futures_leverage_mode'] = leverage_mode
        config['env']['exchanges'][exchanges.SANDBOX]['futures_leverage'] = leverage
    else:
        config['env']['exchanges'][exchanges.SANDBOX]['type'] = 'spot'

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

        assert len(store.completed_trades.trades) == 0

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
