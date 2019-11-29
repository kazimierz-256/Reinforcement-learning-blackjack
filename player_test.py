from game_definitions import Card, Action
import game_logic
import player
import pytest


@pytest.mark.parametrize("player_deck, dealer_card", [
    ([Card.ACE], Card.EIGHT),
    ([Card.TWO, Card.NINE], Card.ACE),
    ([Card.TWO, Card.THREE], Card.ACE),
    ([], Card.JACK),
    ([Card.KING], Card.TWO),
])
def test_player_action_when_small_sum(player_deck, dealer_card):
    player_instance = player.Player()
    # deck_sum = game_logic.evaluate_nonbusting_deck_values(player_deck)
    assert Action.HIT == player_instance.get_action(player_deck, dealer_card)
