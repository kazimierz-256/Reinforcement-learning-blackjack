import numpy as np
import plotly

import game_definitions
import game_logic
from player import Player
import dealer


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 100_000
    # also known as gamma
    discount_factor = 1.0
    random_seed = 123

    np.random.seed(random_seed)

    # blackjack setup
    player = Player()
    for episode_no in range(episode_count):
        game_status, player_visited_bare_states = game_logic.play(player, episode_no)
        player_final_reward = game_logic.get_player_reward(game_status)
        player.end_game_and_update_strategy(
            player_final_reward, player_visited_bare_states, discount_factor)
        if game_status is not game_definitions.Status.DEALER_WON:
            print(game_status)
