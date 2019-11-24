from game import Game, Action, Card
from typing import List, Tuple
import numpy as np


class Player:
    class PlayerStrategy:

        def __init__(self):
            self.state_to_value = {}

        @staticmethod
        def convert_to_state(player_deck, dealer_card):
            player_nonbusting_deck_values = Game.evaluate_nonbusting_deck_values(
                player_deck)
            maximal_nonbusting_player_deck_value = max(
                player_nonbusting_deck_values)
            usable_ace = len(player_nonbusting_deck_values) > 1
            return (maximal_nonbusting_player_deck_value, Game.card_values[dealer_card], usable_ace)

        def get_state_after_hit(self, state):
            raise NotImplementedError()

        def get_state_after_stand(self, state):
            raise NotImplementedError()

        def get_state_value(self, state):
            raise NotImplementedError()
            # return value of state

        def set_state_value(self, state):
            raise NotImplementedError()

        def export_strategy(self):
            # not needed for now
            raise NotImplementedError()

    def __init__(self, strategy: Player_Strategy = None):
        self.strategy = PlayerStrategy.initial_strategy() if strategy is None else strategy

    @staticmethod
    def get_initial_strategy() -> PlayerStrategy:
        return PlayerStrategy.get_initial_strategy()

    def export_strategy(self) -> PlayerStrategy:
        return self.strategy.export_strategy()

    def get_action(
        self,
        player_deck: List[Card],
        dealer_card: Card,
        episode_no: int,
        default_probability_of_stand: float = 0.5
    ) -> Action:

        player_nonbusting_deck_values = Game.evaluate_nonbusting_deck_values(
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

            state = self.strategy.convert_to_state(player_deck, dealer_card)

            # TODO: need to rethink theory behind
            hit_value = self.strategy.get_action_value_from_state(
                state, Action.HIT)
            stand_value = self.strategy.get_action_value_from_state(
                state, Action.STAND)

            player_action = Action.HIT
            # change to Action.STAND only when necessary
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

            return player_action

    def end_game_and_update_strategy(
        self,
        final_reward: float,
        player_visited_bare_states: List[Tuple[List[Card], Card, Action]],
        discount_factor: float
    ):
        # assuming discount factor belongs to the terminal state which is not included in player's strategy
        discounted_reward = discount_factor * final_reward
        for deck, dealer_card, action in reversed(player_visited_bare_states):
            state = Player.PlayerStrategy.convert_to_state(
                deck, Game.card_value[dealer_card], action)
            state_value = self.strategy.get_state_value(state)
            visit_cont = 1 + self.strategy.get_state_visit_count(state)
            new_state_value = (discounted_reward - state_value) / visit_cont
            self.strategy.set_state_value(state, new_state_value)
            self.strategy.increment_state_visit_counter(state)
            # there are no intermediate rewards, so the discounting process is simplified
            discounted_reward *= discount_factor
