from game_definitions import Card
import game_logic
import pytest
import numpy as np


@pytest.mark.parametrize("cards, all_values, nonbusting_values", [
    ([Card.JACK, Card.ACE], [11, 21], [11, 21]),
    ([Card.ACE, Card.ACE],  [2, 12, 22], [2, 12]),
    ([Card.ACE, Card.ACE, Card.ACE, Card.ACE],  [4, 14, 24, 34, 44], [4, 14]),
    ([Card.QUEEN, Card.KING, Card.TWO],  [22], []),
    ([Card.JACK, Card.QUEEN, Card.ACE], [21, 31], [21]),
    ([Card.JACK, Card.ACE, Card.ACE], [12, 22, 32], [12]),
    ([], [0], [0]),
    ([Card.SEVEN, Card.SEVEN, Card.SEVEN], [21], [21]),
    ([Card.SEVEN, Card.SEVEN, Card.EIGHT], [22], []),
    ([Card.TWO], [2], [2]),
])
def test_evaluate_deck_values_busting_and_nonbusting(cards, all_values, nonbusting_values):
    busting_values = list(sorted(game_logic.evaluate_deck_values(cards)))
    assert all_values == busting_values
    nonbusting_values = list(sorted(game_logic.evaluate_nonbusting_deck_values(cards)))
    assert nonbusting_values == nonbusting_values

def test_card_distribution():
    np.random.seed(123)
    for _ in range(100):
        assert game_logic.distribute_card() in Card