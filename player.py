from game_definitions import Card, Action
import game_logic
from typing import List, Tuple
import numpy as np
import strategy

class Player:
    def __init__(self, strategy: strategy.Strategy):
        self.strategy = strategy
    
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    def get_action(
        self,
        player_deck: List[Card],
        dealer_card: Card
    ) -> Action:
        return self.strategy.take_action(player_deck, dealer_card)

    def end_game(
        self,
        final_reward: float,
        player_visited_bare_states: List[Tuple[int, int, Action]],
        discount_factor: float
    ):
        self.strategy.game_finished(final_reward, player_visited_bare_states, discount_factor)
