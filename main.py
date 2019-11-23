import numpy as np
import plotly

from game import Game
from player import Player
from dealer import Dealer


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 100_000
    # also known as gamma
    discount_factor = 0.9
    random_seed = 123

    np.random.seed(random_seed)

    # blackjack setup
    player = Player(Player.get_initial_strategy())
    dealer = Dealer()
    for episode_no in range(episode_count):
        player.prepare_for_new_game()
        game_status, player_deck_action_pairs = Game.play(
            player, dealer, episode_no)
        player_reward = Game.get_player_reward(game_status)
        player.end_game_and_update_strategy(
            player_reward, player_deck_action_pairs, discount_factor)
        print(game_status)
