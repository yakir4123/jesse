# jesse/strategies/RLStrategy.py
import torch
from jesse.strategies import Strategy
from jesse.rl.Agent import Agent  # import RL agent
import jesse.indicators as ta

class RLStrategy(Strategy):

    def __init__(self):
        super().__init__()
        self.agent = Agent(...)  # Initialize RL-agent

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

    def lazy_calc_proba(self):
        pass