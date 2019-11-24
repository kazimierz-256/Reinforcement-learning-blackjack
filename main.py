import numpy as np
import plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import game_definitions
import game_logic
from player import Player
import dealer


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count = 100_000
    print_status_every_n_episodes = 100
    # also known as gamma
    discount_factor = 1.0
    random_seed = 123
    latest_entry_count_for_summary = 100

    np.random.seed(random_seed)

    # blackjack setup
    player = Player(default_probability_of_stand=0.8)
    dealer_win_count = 0
    player_win_count = 0
    player_win_history = []
    player_win_history_average = [0]
    player_win_history_std = []
    # total_player_win_average = 0
    draw_count = 0
    for episode_no in range(episode_count):
        player.probability_of_random_choice = 1E-1  # 1/(1 + episode_no)
        game_status, player_visited_bare_states = game_logic.play(player)
        player_final_reward = game_logic.get_player_reward(game_status)
        player.end_game_and_update_strategy(
            player_final_reward, player_visited_bare_states, discount_factor)

        if game_status == game_definitions.Status.DEALER_WON:
            dealer_win_count += 1
            player_win_history.append(0)

            last_element = player_win_history_average[-1]
            n = len(player_win_history_average)
            player_win_history_average.append(
                last_element + (0-last_element)/n)
            # total_player_win_average += (0-total_player_win_average)/n
        elif game_status == game_definitions.Status.PLAYER_WON:
            player_win_count += 1
            player_win_history.append(1)

            last_element = player_win_history_average[-1]
            n = len(player_win_history_average)
            player_win_history_average.append(
                last_element + (1-last_element)/n)
            # total_player_win_average += (1-total_player_win_average)/n
        elif game_status == game_definitions.Status.DRAW:
            draw_count += 1
        else:
            raise Exception(f"Unexpected game state: {game_status}")

        latest_history = player_win_history_average
        # latest_history = player_win_history_average[-latest_entry_count_for_summary:]
        latest_ratio_average = np.average(latest_history)
        latest_ratio_std = np.std(latest_history)
        player_win_history_std.append(latest_ratio_std)

        # printing all lines at once in order to avoid console text flickering
        messages = [
            f"Latest {latest_entry_count_for_summary} games summary: average player wins/dealer wins: {latest_ratio_average: .5f} standard deviation: {latest_ratio_std: .3E}",
            f"Completed episodes {episode_no + 1} out of {episode_count}"
            # f"Total statistics: average player wins/dealer wins: {total_player_win_average: .5f}"
        ]

        if (episode_no+1) % print_status_every_n_episodes == 0:
            print("\n".join(messages))

    print("Constructing an interactive graph, please wait for a couple of seconds.")
    x = list(range(len(player_win_history)))

    titles = (
        "Total average number of wins since the beginning",
        "Total standerd deviation since the beginning (log plot)"
    )
    fig = make_subplots(rows=2, cols=1, subplot_titles=titles)
    fig.append_trace(go.Scatter(
        x=x,
        y=player_win_history_average
    ), row=1, col=1)
    fig.update_xaxes(title_text="Number of iterations", row=1, col=1)
    fig.update_yaxes(title_text=r"$\text{Total average ratio of player win count to casino win count } (\mu)$", range=[
                     0, 1], row=1, col=1)
    fig.append_trace(go.Scatter(
        x=x,
        y=player_win_history_std
    ), row=2, col=1)
    fig.update_xaxes(title_text="Number of iterations", row=2, col=1)
    fig.update_yaxes(title_text=r"$\text{Total standerd deviation } (\sigma)$", type="log", row=2, col=1)
    fig.update_layout(
        showlegend=False,
        title_text=f"Blackjack Reinforcement Learning algorithm summary after playing {episode_count} games"
    )
    fig.show()
