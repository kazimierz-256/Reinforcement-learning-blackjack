import numpy as np
from enum import Enum, auto, List
import plotly


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

    def get_action(self, player_cards: List[Card], dealer_card: Card, episode_no: int):
        probability_of_random_choice = 1.0/(1 + episode_no)

        state_after_hit = self.strategy.get_state_after_hit()
        state_after_stand = self.strategy.get_state_after_stand()

        hit_state_value = self.strategy.get_state_value(state_after_hit)
        stand_state_value = self.strategy.get_state_value(state_after_stand)

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

    def end_game_and_update_strategy(self, reward: float, gamma: float):
        raise NotImplementedError()


class Dealer:
    @staticmethod
    def get_action(deck: List[Card]):
        deck_values = Game.evaluate_nonbusting_deck_values(deck)
        soft_17_rule_satisfied = max(deck_values) >= 17
        return Action.HIT if soft_17_rule_satisfied else Action.STAND


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

    class Status(Enum):
        PLAYER_WON = auto()
        DEALER_WON = auto()
        DRAW = auto()
        STILL_PLAYING = auto()

    game_status = Status.STILL_PLAYING

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

    def play(self):
        raise NotImplementedError()

    def get_player_reward(self) -> float:
        if self.game_status == Game.Status.DEALER_WON:
            return -1.0
        elif self.game_status == Game.Status.PLAYER_WON:
            return 1.0
        elif self.game_status == Game.Status.DRAW:
            return 0.0
        else:
            raise Exception("The game has not yet ended.")


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 100_000
    gamma = 0.9

    # blackjack setup
    player = Player(Player.get_initial_strategy())
    dealer = Dealer()
    for episode_no in range(episode_count):
        player.prepare_for_new_game()
        game = Game(player, dealer, episode_no)
        game.play()
        player_reward = game.get_player_reward()
        player.end_game_and_update_strategy(player_reward)
