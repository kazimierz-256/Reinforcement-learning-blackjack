import numpy as np
from enum import Enum, auto
from typing import List

import player
import dealer
import game_definitions
import environment_model


def evaluate_deck_values(deck_of_cards: List[game_definitions.Card]) -> List[int]:
    if len(deck_of_cards) == 0:
        return [0]
    else:
        possible_scores = set()
        first_card = deck_of_cards[0]
        first_card_values = game_definitions.card_values[first_card]
        for possibe_rest_of_deck_value in evaluate_deck_values(deck_of_cards[1:]):
            for possible_card_value in first_card_values:
                final_deck_value = possible_card_value + possibe_rest_of_deck_value
                possible_scores.add(final_deck_value)
        return list(possible_scores)


def evaluate_nonbusting_deck_values(deck_of_cards: List[game_definitions.Card]) -> List[int]:
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
        return [0]
    else:
        possible_scores = set()
        first_card = deck_of_cards[0]
        first_card_values = game_definitions.card_values[first_card]
        for possibe_rest_of_deck_value in evaluate_nonbusting_deck_values(deck_of_cards[1:]):
            for possible_card_value in first_card_values:
                final_deck_value = possible_card_value + possibe_rest_of_deck_value
                if final_deck_value < game_definitions.bust_from:
                    possible_scores.add(final_deck_value)
        return list(possible_scores)


def distribute_card():
    # we assume the deck is infinite
    return np.random.choice(game_definitions.Card)


def play(player_instance: player.Player) -> game_definitions.Status:
    def is_deck_busted(deck: List[game_definitions.Card]):
        return len(evaluate_nonbusting_deck_values(deck)) == 0

    # get a card for the dealer
    dealer_deck = [distribute_card()]
    dealers_visible_card = dealer_deck[-1]
    player_deck = [distribute_card()]
    player_visited_bare_states = []
    # successively distribute cards to the player until they hit or bust
    player_deck_busted = False
    while (player_action := player_instance.get_action(player_deck, dealers_visible_card)) == game_definitions.Action.HIT:
        state = environment_model.EnvironmentModel.convert_to_state(player_deck, dealers_visible_card)
        player_instance.strategy.environment_model.increment_state_action_explore_counter(state, player_action)
        player_visited_bare_states.append((state, player_action))
        player_deck.append(distribute_card())
        if is_deck_busted(player_deck):
            player_deck_busted = True
            break
    else:
        state = environment_model.EnvironmentModel.convert_to_state(player_deck, dealers_visible_card)
        player_visited_bare_states.append((state, player_action))
        player_instance.strategy.environment_model.increment_state_action_explore_counter(state, player_action)

    if player_deck_busted:
        return game_definitions.Status.DEALER_WON, player_visited_bare_states
    else:
        # distribute cards to the dealer until they stand or bust
        dealer_deck_busted = False
        while dealer.get_action(dealer_deck) == game_definitions.Action.HIT:
            dealer_deck.append(distribute_card())
            if is_deck_busted(dealer_deck):
                dealer_deck_busted = True
                break

        if dealer_deck_busted:
            return game_definitions.Status.PLAYER_WON, player_visited_bare_states
        else:
            player_values = evaluate_nonbusting_deck_values(
                player_deck)
            dealer_values = evaluate_nonbusting_deck_values(
                dealer_deck)
            player_minus_dealer_score = max(
                player_values) - max(dealer_values)
            if player_minus_dealer_score > 0:
                return game_definitions.Status.PLAYER_WON, player_visited_bare_states
            elif player_minus_dealer_score < 0:
                return game_definitions.Status.DEALER_WON, player_visited_bare_states
            else:
                return game_definitions.Status.DRAW, player_visited_bare_states


def get_player_reward(status: game_definitions.Status) -> float:
    if status == game_definitions.Status.DEALER_WON:
        return -1.0
    elif status == game_definitions.Status.PLAYER_WON:
        return 1.0
    elif status == game_definitions.Status.DRAW:
        return 0.0
    else:
        raise Exception("The game has not yet ended.")
