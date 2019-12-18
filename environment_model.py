from typing import List, Tuple
import numpy as np

import game_logic
import game_definitions

class EnvironmentModel:

    def __init__(self):
        self.state_to_value = {}
        self.state_visit_count = {}
        self.state_explore_count = {}

    @staticmethod
    def convert_to_state(player_deck, dealer_card) -> Tuple[int, int, bool]:
        player_nonbusting_deck_values = game_logic.evaluate_nonbusting_deck_values(
            player_deck)
        maximal_nonbusting_player_deck_value = max(player_nonbusting_deck_values)
        usable_ace = len(player_nonbusting_deck_values) > 1
        # we take the maximum since every maximum value of all cards is unique to that card
        dealer_card_value = max(game_definitions.card_values[dealer_card])
        return (maximal_nonbusting_player_deck_value, dealer_card_value, usable_ace)

    def get_state_action_value(self, state: Tuple[int, int, bool], action: game_definitions.Action) -> float:
        # default value is zero
        return self.state_to_value.get((state, action), 0)

    def set_state_action_value(self, state: Tuple[int, int, bool], action: game_definitions.Action, new_value: float):
        self.state_to_value[(state, action)] = new_value

    def get_state_action_visit_count(self, state: Tuple[int, int, bool], action: game_definitions.Action):
        # default value is zero
        return self.state_visit_count.get((state, action), 0)

    def increment_state_action_visit_counter(self, state: Tuple[int, int, bool], action: game_definitions.Action):
        # there might not be any state saved so I use the getter method insted of checking for existance
        self.state_visit_count[(state, action)] = 1 + self.get_state_action_visit_count(state, action)

    def get_state_action_explore_count(self, state: Tuple[int, int, bool], action: game_definitions.Action):
        # default value is zero
        return self.state_explore_count.get((state, action), 0)

    def increment_state_action_explore_counter(self, state: Tuple[int, int, bool], action: game_definitions.Action):
        # there might not be any state saved so I use the getter method insted of checking for existance
        self.state_explore_count[(state, action)] = 1 + self.get_state_action_explore_count(state, action)