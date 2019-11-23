from game import Game, Action, Card
from typing import List, Tuple
import numpy as np


class Player:
    class PlayerStrategy:
        @staticmethod
        def get_initial_strategy():
            raise NotImplementedError()

        @staticmethod
        def encode_deck_action_pair_to_state(deck, action):
            raise NotImplementedError()

        def get_state_after_hit(self, state):
            raise NotImplementedError()

        def get_state_after_stand(self, state):
            raise NotImplementedError()

        def get_state_value(self, state):
            raise NotImplementedError()
            # return value of state

        def set_state_value(self, state):
            raise NotImplementedError()

    def __init__(self, strategy: Player_Strategy):
        self.strategy = strategy
        self.state_action_sequence = []

    @staticmethod
    def get_initial_strategy() -> PlayerStrategy:
        return PlayerStrategy.get_initial_strategy()

    def export_strategy(self) -> PlayerStrategy:
        raise NotImplementedError()

    def prepare_for_new_game(self):
        self.state_action_sequence.clear()

    def get_action(self, player_deck: List[Card], dealer_card: Card, episode_no: int):

        player_deck_values = Game.evaluate_nonbusting_deck_values(player_deck)
        maximal_nonbusting_player_deck_value = max(player_deck_values)

        if maximal_nonbusting_player_deck_value <= 10:
            # it is always disadvantageous for the player to stand when their deck score does not exceed 11
            return Action.HIT
        else:
            probability_of_random_choice = 1.0/(1 + episode_no)

            state_after_hit = self.strategy.get_state_after_hit()
            state_after_stand = self.strategy.get_state_after_stand()

            hit_state_value = self.strategy.get_state_value(state_after_hit)
            stand_state_value = self.strategy.get_state_value(
                state_after_stand)

            player_action = Action.HIT
            if np.random.random() < probability_of_random_choice:
                # act randomly
                if np.random.random() < 0.5:
                    player_action = Action.STAND
            else:
                # act greedily
                if stand_state_value > hit_state_value:
                    player_action = Action.STAND

            raise NotImplementedError()

    def end_game_and_update_strategy(self, reward: float, player_deck_action_pairs: List[Tuple[List[Card], Action]], discount_factor: float):
        raise NotImplementedError()
