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

    @staticmethod
    def distribute_card():
        # we assume the deck is infinite
        return np.random.choice(Card)

    @staticmethod
    def play(self, player: Player, dealer: Dealer, episode_no: int) -> Game.Status:
        def is_deck_busted(deck: List[Card]):
            return len(Game.evaluate_nonbusting_deck_values(player_deck)) == 0
        # get a card for the dealer
        dealer_deck = [Game.distribute_card()]
        player_deck = []
        # successively distribute cards to the player until they hit or bust
        player_deck_busted = False
        while player.get_action(player_deck, dealer_deck[-1], episode_no) != Action.HIT:
            player_deck.append(Game.distribute_card())
            if is_deck_busted(player_deck):
                player_deck_busted = True
                break

        if player_deck_busted:
            return Game.Status.DEALER_WON
        else:
            # distribute cards to the dealer until they hit or bust
            dealer_deck_busted = False
            while dealer.get_action(dealer_deck) != Action.HIT:
                dealer_deck.append(Game.distribute_card())
                if is_deck_busted(dealer_deck):
                    dealer_deck_busted = True
                    break

            if dealer_deck_busted:
                return Game.Status.PLAYER_WON
            else:
                player_values = Game.evaluate_nonbusting_deck_values(
                    player_deck)
                dealer_values = Game.evaluate_nonbusting_deck_values(
                    dealer_deck)
                player_minus_dealer_score = max(
                    player_values) - max(dealer_values)
                if player_minus_dealer_score > 0:
                    return Game.Status.PLAYER_WON
                elif player_minus_dealer_score < 0:
                    return Game.Status.DEALER_WON
                else:
                    return Game.Status.DRAW

    @staticmethod
    def get_player_reward(status: Game.Status) -> float:
        if status == Game.Status.DEALER_WON:
            return -1.0
        elif status == Game.Status.PLAYER_WON:
            return 1.0
        elif status == Game.Status.DRAW:
            return 0.0
        else:
            raise Exception("The game has not yet ended.")


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 100_000
    # also known as gamma
    discount_factor = 0.9

    # blackjack setup
    player = Player(Player.get_initial_strategy())
    dealer = Dealer()
    for episode_no in range(episode_count):
        player.prepare_for_new_game()
        game_status = Game.play(player, dealer, episode_no)
        player_reward = Game.get_player_reward(game_status)
        player.end_game_and_update_strategy(player_reward)
