from game import Game, Action


class Dealer:
    @staticmethod
    def get_action(deck: List[Card]):
        deck_values = Game.evaluate_nonbusting_deck_values(deck)
        soft_17_rule_satisfied = max(deck_values) >= 17
        return Action.HIT if soft_17_rule_satisfied else Action.STAND
