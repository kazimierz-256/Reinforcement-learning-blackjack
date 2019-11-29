import numpy as np
import plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import game_definitions
import game_logic
from player import Player
import dealer
import typing


def draw_figure(player_win_history, player_win_history_average, player_win_history_std):
    # figure drawing part
    print("Constructing an interactive graph, please wait for a couple of seconds.")
    x = list(range(len(player_win_history)))

    titles = (
        "Total average number of wins since the beginning",
        "Total standard deviation since the beginning (log plot)"
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
    fig.update_yaxes(
        title_text=r"$\text{Total standard deviation } (\sigma)$", type="log", row=2, col=1)
    fig.update_layout(
        showlegend=False,
        title_text=f"Blackjack Reinforcement Learning algorithm summary after playing {episode_count} games"
    )
    if show_plots_in_browser_tab:
        fig.show()


def draw_strategy_heatmap(strategy: Player.Strategy):
    def get_matrix_dealer_value_player_sum(usable_ace: bool, action: game_definitions.Action):
        matrix = np.zeros(
            (
                len(game_definitions.Card),
                game_definitions.bust_from
            )
        )
        for player_sum in range(2, game_definitions.bust_from):
            if not (usable_ace and player_sum < 11):
                card_maximum_values = (max(game_definitions.card_values[card]) for card in game_definitions.Card)
                for dealer_card_value in set(card_maximum_values):
                    state = (player_sum, dealer_card_value, usable_ace)
                    state_action_value = strategy.get_state_action_value(state, action)
                    matrix[dealer_card_value, player_sum] = state_action_value
        return matrix
    print("Drawing heatmaps...")
    titles = ("Unusable ace, HIT", "Unusable ace, STAND", "Usable ace, HIT", "Usable ace, STAND")
    fig = make_subplots(rows=2, cols=2, subplot_titles=titles)
    xs = [f"player sum {i}" for i in range(2, game_definitions.bust_from)]
    ys = [f"dealer card value {i}" for i in range(2, 12)]
    for row, usable_ace in enumerate([False, True]):
        for column, action in enumerate([game_definitions.Action.HIT, game_definitions.Action.STAND]):
            matrix = get_matrix_dealer_value_player_sum(usable_ace, action)
            heatmap = go.Heatmap(z=matrix, x=xs, y=ys)
            fig.add_trace(heatmap, row=row+1, col=column+1)
    fig.show()
    print("Done drawing heatmaps")


if __name__ == "__main__":

    # reinforcement learning parameters
    episode_count_list = [200_000]
    print_status_every_n_episodes = 10_000
    # also known as gamma
    discount_factor = 1.0
    random_seed = 123
    latest_entry_count_for_summary = 100
    show_plots_in_browser_tab = True
    probability_of_random_choice_list = [5E-2]
    default_probability_of_stand = .5

    np.random.seed(random_seed)

    for episode_count in episode_count_list:
        for probability_of_random_choice in probability_of_random_choice_list:
            export_plot_name = f"discount_factor-{discount_factor},episodes-{episode_count},seed-{random_seed}"

            # initial setup
            player_instance = Player(default_probability_of_stand=default_probability_of_stand)
            dealer_win_count = 0
            player_win_count = 0
            player_win_history = []
            player_win_history_average = [0]
            player_win_history_std = []
            # total_player_win_average = 0
            draw_count = 0

            # playing blackjack games
            for episode_no in range(episode_count):
                # 1/(1 + episode_no) #probability_of_random_choice
                player_instance.probability_of_random_choice = probability_of_random_choice
                game_status, player_visited_bare_states = game_logic.play(
                    player_instance)
                player_final_reward = game_logic.get_player_reward(game_status)
                player_instance.end_game_and_update_strategy(
                    player_final_reward, player_visited_bare_states, discount_factor)

                # game ended, check who has won the game
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

                latest_history = player_win_history
                # latest_history = player_win_history_average[-latest_entry_count_for_summary:]
                latest_ratio_average = np.average(latest_history)
                latest_ratio_std = np.std(latest_history)
                player_win_history_std.append(latest_ratio_std)

                # printing all lines at once in order to avoid console text flickering
                messages = [
                    f"Latest {latest_entry_count_for_summary} games summary: average player wins/dealer wins: {latest_ratio_average: .5f} standard deviation: {latest_ratio_std: .3E}",
                    f"Completed episodes {episode_no + 1} out of {episode_count}",
                    str(len(player_instance.strategy.state_to_value))
                    # f"Total statistics: average player wins/dealer wins: {total_player_win_average: .5f}"
                ]

                if (episode_no+1) % print_status_every_n_episodes == 0:
                    print("\n".join(messages))
                    draw_strategy_heatmap(player_instance.strategy)

            draw_figure(player_win_history,
                        player_win_history_average, player_win_history_std)
