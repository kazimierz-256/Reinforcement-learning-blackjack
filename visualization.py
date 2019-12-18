import numpy as np

import plotly as py
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import game_definitions
import player
import environment_model

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


def draw_strategy_heatmap(envmodel: environment_model.EnvironmentModel):
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
                    state_action_value = envmodel.get_state_action_value(state, action)
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