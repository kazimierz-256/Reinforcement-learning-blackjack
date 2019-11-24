from game_definitions import Card, Action
import game_logic
from typing import List, Tuple
import numpy as np


class Player:
    class Strategy:

        def __init__(self):
            self.state_to_value = {}
            self.state_visit_count = {}

        @staticmethod
        def convert_to_state(player_deck, dealer_card):
            player_nonbusting_deck_values = game_logic.evaluate_nonbusting_deck_values(
                player_deck)
            maximal_nonbusting_player_deck_value = max(
                player_nonbusting_deck_values)
            usable_ace = len(player_nonbusting_deck_values) > 1
            return (maximal_nonbusting_player_deck_value, dealer_card, usable_ace)

        def get_state_action_value(self, state, action):
            # default value is zero
            return self.state_to_value.get((state, action), 0)

        def set_state_action_value(self, state, action, new_value):
            self.state_to_value[(state, action)] = new_value

        def get_state_action_visit_count(self, state, action):
            # default value is zero
            return self.state_visit_count.get((state, action), 0)

        def increment_state_action_visit_counter(self, state, action):
            # there might not be any state saved so I use the getter method insted of checking for existance
            self.state_visit_count[(state, action)] = 1 + self.get_state_action_visit_count(state, action)

        def export_strategy(self):
            # not needed for now
            raise NotImplementedError()

    def __init__(self, strategy=None):
        self.strategy = Player.Strategy() if strategy is None else strategy

    @staticmethod
    def get_initial_strategy() -> Strategy:
        return Strategy.get_initial_strategy()

    def export_strategy(self) -> Strategy:
        return self.strategy.export_strategy()

    def get_action(
        self,
        player_deck: List[Card],
        dealer_card: Card,
        episode_no: int,
        default_probability_of_stand: float = 0.5
    ) -> Action:

        player_nonbusting_deck_values = game_logic.evaluate_nonbusting_deck_values(
            player_deck)
        maximal_nonbusting_player_deck_value = max(
            player_nonbusting_deck_values)

        if maximal_nonbusting_player_deck_value <= 10:
            # it is always disadvantageous for the player to stand when their deck score does not exceed 11
            return Action.HIT
        else:
            # the sum of 1/k increases without bound yet the sum 1/k^2 is finite
            # which ensures convergence
            probability_of_random_choice = 1.0/(1 + episode_no)

            state = Player.Strategy.convert_to_state(player_deck, dealer_card)

            hit_value = self.strategy.get_state_action_value(
                state, Action.HIT)
            stand_value = self.strategy.get_state_action_value(
                state, Action.STAND)

            # one could implicitly initialize a variable from nested scope
            # but I prefer explicit variable initialization
            # but then choosing a default action and only changing it when necessary
            # yields an asymmetric solution
            # but using an inner method makes the cases symmetric and explicit
            # in the end it is a trade-off
            def choose_player_action():
                if np.random.random() <= probability_of_random_choice:
                    # act randomly
                    if np.random.random() <= default_probability_of_stand:
                        player_action = Action.STAND
                else:
                    # act greedily
                    if stand_value > hit_value:
                        player_action = Action.STAND
                    elif stand_value == hit_value:
                        # break ties
                        if np.random.random() <= default_probability_of_stand:
                            player_action = Action.STAND
                return Action.HIT

            return choose_player_action()

    def end_game_and_update_strategy(
        self,
        final_reward: float,
        player_visited_bare_states: List[Tuple[List[Card], Card, Action]],
        discount_factor: float
    ):
        # assuming discount factor belongs to the terminal state which is not included in player's strategy
        discounted_reward = discount_factor * final_reward
        for deck, dealer_card, action in reversed(player_visited_bare_states):
            state = Player.Strategy.convert_to_state(deck, dealer_card)
            state_value = self.strategy.get_state_action_value(state, action)
            visit_cont = 1 + self.strategy.get_state_action_visit_count(state, action)
            new_state_value = (discounted_reward - state_value) / visit_cont
            self.strategy.set_state_action_value(state, action, new_state_value)
            self.strategy.increment_state_action_visit_counter(state, action)
            # there are no intermediate rewards, so the discounting process is simplified
            discounted_reward *= discount_factor
