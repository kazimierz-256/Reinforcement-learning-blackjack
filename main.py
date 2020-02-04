import numpy as np

import typing

import game_definitions
import game_logic
import player
import dealer
import visualization
import random_learning_strategy
import random_fixed_strategy
import environment_model


if __name__ == "__main__":
    # reinforcement learning parameters
    episode_count_list = [100_000]
    print_status_every_n_episodes = 10_000
    # also known as gamma
    discount_factor = 1.0
    learning_rate = 0.1
    random_seed = 123
    latest_entry_count_for_summary = 10_000_000
    show_plots_in_browser_tab = True
    probability_of_random_choice_list = [0.1]
    default_probability_of_stand = .5

    np.random.seed(random_seed)

    for episode_count in episode_count_list:
        for probability_of_random_choice in probability_of_random_choice_list:
            export_plot_name = f"discount_factor-{discount_factor},episodes-{episode_count},seed-{random_seed}"

            # initial setup
            player_environment_model = environment_model.EnvironmentModel()
            player_fixed_strategy = random_fixed_strategy.Random_fixed_strategy(
                environment_model=player_environment_model,
                default_probability_of_stand=default_probability_of_stand
                )
            player_learning_strategy = random_learning_strategy.Random_learning_strategy(
                environment_model=player_environment_model,
                probability_of_random_choice=probability_of_random_choice,
                default_probability_of_stand=default_probability_of_stand
                )
                
            player_instance = player.Player(strategy=player_learning_strategy)
            dealer_win_count = 0
            player_win_count = 0
            player_win_history = []
            player_win_history_average = [0]
            player_win_history_std = []
            # total_player_win_average = 0
            draw_count = 0

            # playing blackjack games with fixed strategy
            for episode_no in range(episode_count):
                # 1/(1 + episode_no) #probability_of_random_choice
                player_instance.probability_of_random_choice = probability_of_random_choice
                game_status, player_visited_bare_states = game_logic.play(player_instance)
                player_final_reward = game_logic.get_player_reward(game_status)
                player_instance.end_game(
                    player_final_reward,
                    player_visited_bare_states,
                    discount_factor,
                    learning_rate
                    )

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
                    str(len(player_environment_model.state_to_value))
                    # f"Total statistics: average player wins/dealer wins: {total_player_win_average: .5f}"
                ]

                if (episode_no+1) % print_status_every_n_episodes == 0:
                    print("\n".join(messages))
                    visualization.draw_strategy_heatmap(player_environment_model)

            # print("Learning from fixed strategy")

            # # playing blackjack games and learning
            # for episode_no in range(episode_count):
            #     # 1/(1 + episode_no) #probability_of_random_choice
            #     player_instance.probability_of_random_choice = probability_of_random_choice
            #     game_status, player_visited_bare_states = game_logic.play(player_instance)
            #     player_final_reward = game_logic.get_player_reward(game_status)
            #     player_instance.end_game(
            #         player_final_reward, player_visited_bare_states, discount_factor, learning_rate)

            #     # game ended, check who has won the game
            #     if game_status == game_definitions.Status.DEALER_WON:
            #         dealer_win_count += 1
            #         player_win_history.append(0)

            #         last_element = player_win_history_average[-1]
            #         n = len(player_win_history_average)
            #         player_win_history_average.append(
            #             last_element + (0-last_element)/n)
            #         # total_player_win_average += (0-total_player_win_average)/n
            #     elif game_status == game_definitions.Status.PLAYER_WON:
            #         player_win_count += 1
            #         player_win_history.append(1)

            #         last_element = player_win_history_average[-1]
            #         n = len(player_win_history_average)
            #         player_win_history_average.append(
            #             last_element + (1-last_element)/n)
            #         # total_player_win_average += (1-total_player_win_average)/n
            #     elif game_status == game_definitions.Status.DRAW:
            #         draw_count += 1
            #     else:
            #         raise Exception(f"Unexpected game state: {game_status}")

            #     latest_history = player_win_history
            #     # latest_history = player_win_history_average[-latest_entry_count_for_summary:]
            #     latest_ratio_average = np.average(latest_history)
            #     latest_ratio_std = np.std(latest_history)
            #     player_win_history_std.append(latest_ratio_std)

            #     # printing all lines at once in order to avoid console text flickering
            #     messages = [
            #         f"Latest {latest_entry_count_for_summary} games summary: average player wins/dealer wins: {latest_ratio_average: .5f} standard deviation: {latest_ratio_std: .3E}",
            #         f"Completed episodes {episode_no + 1} out of {episode_count}",
            #         str(len(player_environment_model.state_to_value))
            #         # f"Total statistics: average player wins/dealer wins: {total_player_win_average: .5f}"
            #     ]

            #     if (episode_no+1) % print_status_every_n_episodes == 0:
            #         print("\n".join(messages))
            #         visualization.draw_strategy_heatmap(player_environment_model)



            if show_plots_in_browser_tab:
                visualization.draw_figure(
                    player_win_history,
                    player_win_history_average,
                    player_win_history_std,
                    episode_count
                    )
