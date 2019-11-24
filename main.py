import numpy as np
import plotly

from game import Game
from player import Player
from dealer import Dealer


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 100_000
    # also known as gamma
    discount_factor = 1.0
    random_seed = 123

    np.random.seed(random_seed)

    # blackjack setup
    player = Player()
    dealer = Dealer()
    for episode_no in range(episode_count):
        game_status, player_visited_bare_states = Game.play(
            player, dealer, episode_no)
        player_final_reward = Game.get_player_reward(game_status)
        player.end_game_and_update_strategy(
            player_final_reward, player_visited_bare_states, discount_factor)
        print(game_status)
