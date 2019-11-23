import numpy as np
from enum import Enum, auto, List
import plotly

# jack, queen, king = 10, ace = 1 or 11
# blackjack: ace + 10-value card gives a 50% bonus
# https://towardsdatascience.com/playing-blackjack-using-model-free-reinforcement-learning-in-google-colab-aa2041a2c13d


class Card(Enum):
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    QUEEN = auto()
    KING = auto()
    JACK = auto()
    ACE = auto()


class Action(Enum):
    HIT = auto()
    STAND = auto()


class Player:
    class Player_Strategy:
        @staticmethod
        def get_initial_strategy():
            raise NotImplementedError()

    def __init__(self, strategy: Player_Strategy):
        self.strategy = strategy

    @staticmethod
    def get_initial_strategy() -> Player_Strategy:
        return Player_Strategy.get_initial_strategy()

    def export_strategy(self) -> Player_Strategy:
        raise NotImplementedError()

    def initialize_game(self, initial_card: Card):
        raise NotImplementedError()

    def add_card(self, card: Card):
        raise NotImplementedError()

    def get_action(self, dealers_card: Card, episode: int):
        probability_of_greedy_choice = 1.0-1/episode
        if np.random.random() < probability_of_greedy_choice:
            # act greedily
            pass
        else:
            # do not act greedily
            pass

    def end_game_and_reward_player(self, reward: float, gamma: float):
        raise NotImplementedError()


class Dealer:
    def __init__(self, initial_card: Card):
        super().__init__()

    def add_card(self, card: Card):
        raise NotImplementedError()

    def get_action(self):
        raise NotImplementedError()


class Game:
    Game.card_values = {
        Card.TWO: [2],
        Card.THREE: [3],
        Card.FOUR: [4],
        Card.FIVE: [5],
        Card.SIX: [6],
        Card.SEVEN: [7],
        Card.EIGHT: [8],
        Card.NINE: [9],
        Card.TEN: [10],
        Card.QUEEN: [10],
        Card.KING: [10],
        Card.JACK: [10],
        Card.ACE: [1, 11],
    }
    Game.bust_from = 22

    @staticmethod
    def evaluate_deck_values(deck_of_cards: List[Card]) -> List[int]:
        if len(deck_of_cards) == 0:
            return 0
        else:
            possible_scores = {}
            first_card = deck_of_cards[0]
            first_card_values = Game.card_values[first_card]
            for possible_card_value in first_card_values:
                final_deck_value = possible_card_value + \
                    evaluate_deck_values(deck_of_cards[1:])
                possible_scores.add(final_deck_value)
            return list(possible_scores)

    @staticmethod
    def evaluate_nonbusting_deck_values(deck_of_cards: List[Card]) -> List[int]:
        all_possible_values = Game.evaluate_deck_values(deck_of_cards)
        return [value for value in all_possible_values if value >= Game.bust_from]

    @staticmethod
    def is_terminal_state(player_cards, dealer_cards):
        raise NotImplementedError()

    @staticmethod
    def get_next_state_and_reward(state, action):
        raise NotImplementedError()

    @staticmethod
    def get_possible_actions(state):
        raise NotImplementedError()


if __name__ == "__main__":
    raise NotImplementedError()
