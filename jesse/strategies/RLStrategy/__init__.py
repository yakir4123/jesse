# jesse/strategies/RLStrategy.py
from typing import List, Dict

import torch

import jesse.indicators as ta
from jesse.models import Route, Position, Order
from jesse.rl.Agent import Agent  # import RL agent
from jesse.store import ClosedTrades
from jesse.strategies import Strategy


class RLStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.agent = Agent(
            MODEL='ddqn',
            DOUBLE=True,

        )  # Initialize RL-agent

    # region Agent

    # def select_action(self, state):
    #     pass

    # def optimize_model(self):
    #     pass

    # def optimize_double_dqn_model(self):
    #     pass

    # def train(self, env, path, num_episodes=40):
    #     pass

    # def test(self, env_test, model_name=None, path=None):
    #     pass

    # endregion

    # region Strategy
    # def hyperparameters(self) -> list:
    #     return []
    #
    # def dna(self) -> str:
    #     return ''

    @property
    def is_short(self) -> bool:
        action = self.agent.select_action(self.get_state())  # Get RL-agent state
        if action == 2:  # Sell action
            return True
        return False

    @property
    def is_long(self) -> bool:
        action = self.agent.select_action(self.get_state())  # Get RL-agent state
        if action == 1:  # Buy action
            return True
        return False

    def should_long(self) -> bool:
        if self.is_long and not self.is_short:
            return True
        return None

    def should_short(self) -> bool:
        if self.is_short and not self.is_long:
            return True
        return None

    def should_cancel(self):
        return False

    def go_long(self):
        # qty = self.available_margin * 0.99
        qty = 0.01
        self.buy = qty, self.price
        pass

    def go_short(self):
        # qty = self.available_margin * 0.99
        qty = 0.01
        self.sell = qty, self.price
        pass

    def get_state(self):
        # Market state
        # Example: using last close, volume and RSI
        close = self.candles[:, 2]
        volume = self.candles[:, 5]
        rsi = ta.rsi(close, period=14)

        # create PyTorch tensor
        # Now model support only close price prediction
        state = torch.tensor([close[-1]])

        # TODO
        # state = torch.tensor([close[-1], volume[-1], rsi[-1]])
        return state


    #
    # def lazy_calc_proba(self):
    #     pass
    #
    # def has_long_entry_orders(self) -> bool:
    #     pass
    #
    # def has_short_entry_orders(self) -> bool:
    #     pass
    #
    # def liquidate(self):
    #     pass
    #
    # def routes(self) -> List[Route]:
    #     pass
    #
    # def leverage(self) -> int:
    #     pass
    #
    # def all_positions(self) -> Dict[str, Position]:
    #     pass
    #
    # def portfolio_value(self) -> float:
    #     pass
    #
    # def trades(self) -> List[ClosedTrades]:
    #     pass
    #
    # def orders(self) -> List[Order]:
    #     pass
    #
    # def entry_orders(self):
    #     pass
    #
    # def exit_orders(self):
    #     pass
    #
    # def active_exit_orders(self):
    #     pass
    #
    # def exchange_type(self):
    #     pass
    #
    # def is_spot_trading(self) -> bool:
    #     pass
    #
    # def is_futures_trading(self) -> bool:
    #     pass
    #
    # def daily_balances(self):
    #     pass
    #
    # def is_backtesting(self) -> bool:
    #     pass
    #
    # def is_livetrading(self) -> bool:
    #     pass
    #
    # def is_papertrading(self) -> bool:
    #     pass
    #
    # def is_live(self) -> bool:
    #     pass
    #
    # def min_qty(self) -> float:
    #     pass

    # endregion