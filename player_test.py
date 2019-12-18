import pytest

import environment_model
import game_definitions
import random_learning_strategy


@pytest.mark.parametrize("player_deck, dealer_card", [
    ([game_definitions.Card.ACE], game_definitions.Card.EIGHT),
    ([game_definitions.Card.TWO, game_definitions.Card.NINE], game_definitions.Card.ACE),
    ([game_definitions.Card.TWO, game_definitions.Card.THREE], game_definitions.Card.ACE),
    ([], game_definitions.Card.JACK),
    ([game_definitions.Card.KING], game_definitions.Card.TWO),
])
def test_player_action_when_small_sum(player_deck, dealer_card):
    em = environment_model.EnvironmentModel()
    learning_strategy = random_learning_strategy.Random_learning_strategy(
        environment_model=em,
        probability_of_random_choice=.5,
        default_probability_of_stand=.5
        )
    # deck_sum = game_logic.evaluate_nonbusting_deck_values(player_deck)
    assert game_definitions.Action.HIT == learning_strategy.take_action(player_deck, dealer_card)
