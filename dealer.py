from game_definitions import Action, Card
from typing import List
import game_logic

def get_action(deck: List[Card]):
    deck_values = game_logic.evaluate_nonbusting_deck_values(deck)
    soft_17_rule_satisfied = max(deck_values) >= 17
    return Action.STAND if soft_17_rule_satisfied else Action.HIT
