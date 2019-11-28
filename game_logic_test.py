from game_definitions import Card
import game_logic
import pytest


@pytest.mark.parametrize("cards,reference_values", [
    ([Card.JACK, Card.ACE], [11, 21]),
    ([Card.JACK, Card.ACE, Card.ACE], [12, 22, 32]),
])
def test_evaluate_deck_values(cards, reference_values):
    values = list(sorted(game_logic.evaluate_deck_values(cards)))
    assert reference_values == values


@pytest.mark.parametrize("cards,reference_values", [
    ([Card.JACK, Card.ACE, Card.ACE], [12]),
])
def test_evaluate_deck_values_nonbusting(cards, reference_values):
    values = list(sorted(game_logic.evaluate_nonbusting_deck_values(cards)))
    assert reference_values == values
