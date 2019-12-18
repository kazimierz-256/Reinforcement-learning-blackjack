from typing import List, Tuple
import game_definitions

class Strategy:
    """ An interface that represents player's strategy and their reaction after the game ended """

    def take_action(
        self,
        player_deck: List[game_definitions.Card],
        dealer_card: game_definitions.Card
        ) -> game_definitions.Action:
            raise NotImplementedError()

    def game_finished(
        self,
        final_reward: float,
        player_visited_bare_states: List[Tuple[int, int, game_definitions.Action]],
        discount_factor: float
        ):
            raise NotImplementedError()