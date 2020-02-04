import numpy as np

from typing import List, Tuple

import strategy
import game_logic
import game_definitions
import environment_model

class Random_fixed_strategy(strategy.Strategy):
    
    def __init__(
            self,
            environment_model: environment_model.EnvironmentModel,
            default_probability_of_stand: float
            ):
        super().__init__()
        self.environment_model = environment_model
        self.default_probability_of_stand = default_probability_of_stand

    @property
    def environment_model(self):
        return self._environment_model

    @environment_model.setter
    def environment_model(self, value):
        self._environment_model = value

    def take_action(
        self,
        player_deck: List[game_definitions.Card],
        dealer_card: game_definitions.Card
        ) -> game_definitions.Action:

        maximal_nonbusting_player_deck_value = max(
            game_logic.evaluate_nonbusting_deck_values(player_deck)
        )

        if maximal_nonbusting_player_deck_value <= 11:
            # it is always disadvantageous for the player to stand when their deck score does not exceed 11
            return game_definitions.Action.HIT
        else:
            # the sum of 1/k increases without bound yet the sum 1/k^2 is finite
            # which ensures convergence

            state = environment_model.EnvironmentModel.convert_to_state(player_deck, dealer_card)

            hit_value = self.environment_model.get_state_action_value(
                state, game_definitions.Action.HIT)
            stand_value = self.environment_model.get_state_action_value(
                state, game_definitions.Action.STAND)

            # act greedily
            if stand_value > hit_value:
                return game_definitions.Action.STAND
            elif stand_value == hit_value:
                # break ties
                if np.random.random() <= self.default_probability_of_stand:
                    return game_definitions.Action.STAND
            return game_definitions.Action.HIT

        # avoiding bust strategy
        # return game_definitions.Action.STAND if maximal_nonbusting_player_deck_value >= 12 else game_definitions.Action.HIT

    def game_finished(
        self,
        final_reward: float,
        player_visited_bare_states: List[Tuple[int, int, game_definitions.Action]],
        discount_factor: float,
        learning_rate: float
        ):
        # assuming discount factor belongs to the terminal state which is not included in player's environment_model
        discounted_reward = final_reward
        for state, action in reversed(player_visited_bare_states):

            state_value = self.environment_model.get_state_action_value(state, action)
            visit_count = 1 + self.environment_model.get_state_action_visit_count(state, action)
            new_state_value = (1 - learning_rate) * state_value + learning_rate * (discounted_reward - state_value)
            self.environment_model.set_state_action_value(state, action, new_state_value)
            self.environment_model.increment_state_action_visit_counter(state, action)
            # there are no intermediate rewards, so the discounting process is simplified
            # unsure whether this is the right formula, need to verify
            discounted_reward = new_state_value * discount_factor