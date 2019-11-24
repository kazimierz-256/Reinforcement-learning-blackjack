import numpy as np
import plotly

import game_definitions
import game_logic
from player import Player
import dealer


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 1_000_000
    # also known as gamma
    discount_factor = 1.0
    random_seed = 123

    np.random.seed(random_seed)

    # blackjack setup
    player = Player()
    dealer_win_count = 0
    player_win_count = 0
    draw_count = 0
    for episode_no in range(episode_count):
        game_status, player_visited_bare_states = game_logic.play(player, episode_no)
        player_final_reward = game_logic.get_player_reward(game_status)
        player.end_game_and_update_strategy(
            player_final_reward, player_visited_bare_states, discount_factor)
        if game_status == game_definitions.Status.DEALER_WON:
            dealer_win_count += 1
        elif game_status == game_definitions.Status.PLAYER_WON:
            player_win_count += 1
        elif game_status == game_definitions.Status.DRAW:
            draw_count += 1
        else:
            raise Exception(f"Unexpected game state: {game_status}")
        print(player_win_count / dealer_win_count)
