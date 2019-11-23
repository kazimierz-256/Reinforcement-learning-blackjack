from enum import Enum, auto, List
import numpy as np


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
            possible_scores = set()
            first_card = deck_of_cards[0]
            first_card_values = Game.card_values[first_card]
            for possible_card_value in first_card_values:
                final_deck_value = possible_card_value + \
                    evaluate_deck_values(deck_of_cards[1:])
                possible_scores.add(final_deck_value)
            return list(possible_scores)

    @staticmethod
    def evaluate_nonbusting_deck_values(deck_of_cards: List[Card]) -> List[int]:
        """
        For readibility this method could have called evaluate_deck_values()
        and then filter out the result based on whether or not the deck causes busting
        but for this way the deck will never exceed the limit and
        the value of each excess ace card will have to become 1

        I perfectly know that therey may be at most one usable ace at a given time
        nevertheless the solutions I have seen on the internet use too many magic numbers
        and they do not scale, as opposed to a mathematically appealing solution provided below
        it is a trade-off between oversimplified logic and mathematical elegance/self-explanatory code
        I deliberately chose to implement a mathematically appealing and self-explanatory code
        """
        if len(deck_of_cards) == 0:
            return 0
        else:
            possible_scores = set()
            first_card = deck_of_cards[0]
            first_card_values = Game.card_values[first_card]
            for possible_card_value in first_card_values:
                final_deck_value = possible_card_value + \
                    evaluate_nonbusting_deck_values(deck_of_cards[1:])
                if final_deck_value <= Game.bust_from:
                    possible_scores.add(final_deck_value)
            return list(possible_scores)

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

        def get_player_deck():
            return (player_deck.copy(), dealers_visible_card)
        # get a card for the dealer
        dealer_deck = [Game.distribute_card()]
        player_deck = []
        dealers_visible_card = dealer_deck[-1]
        player_visited_bare_states = []
        # successively distribute cards to the player until they hit or bust
        player_deck_busted = False
        while player_action := player.get_action(player_deck, dealers_visible_card, episode_no) == Action.HIT:
            player_visited_bare_states.append((get_player_deck(), dealers_visible_card, player_action))
            player_deck.append(Game.distribute_card())
            if is_deck_busted(player_deck):
                player_deck_busted = True
                break

        if player_deck_busted:
            return Game.Status.DEALER_WON, player_visited_bare_states
        else:
            # distribute cards to the dealer until they stand or bust
            dealer_deck_busted = False
            while dealer.get_action(dealer_deck) == Action.HIT:
                dealer_deck.append(Game.distribute_card())
                if is_deck_busted(dealer_deck):
                    dealer_deck_busted = True
                    break

            if dealer_deck_busted:
                return Game.Status.PLAYER_WON, player_visited_bare_states
            else:
                player_values = Game.evaluate_nonbusting_deck_values(
                    player_deck)
                dealer_values = Game.evaluate_nonbusting_deck_values(
                    dealer_deck)
                player_minus_dealer_score = max(
                    player_values) - max(dealer_values)
                if player_minus_dealer_score > 0:
                    return Game.Status.PLAYER_WON, player_visited_bare_states
                elif player_minus_dealer_score < 0:
                    return Game.Status.DEALER_WON, player_visited_bare_states
                else:
                    return Game.Status.DRAW, player_visited_bare_states

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
