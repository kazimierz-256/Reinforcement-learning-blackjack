from game_definitions import Card
import game_logic
import unittest

class TestDeckValues(unittest.TestCase):

    def test_evaluate_deck_values1(self):
        values = list(sorted(game_logic.evaluate_deck_values([Card.JACK, Card.ACE])))
        self.assertEqual(values, [11, 21])

    def test_evaluate_deck_values2(self):
        values = list(sorted(game_logic.evaluate_deck_values([Card.JACK, Card.ACE, Card.ACE])))
        self.assertEqual(values, [12, 22, 32])

if __name__ == '__main__':
    unittest.main()