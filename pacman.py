import random

import game_engine
import agents
import numpy as np
import matplotlib.pyplot as plt
import os  

# Headless mode avoids opening many windows when benchmarking in parallel.
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')

if __name__ == "__main__":
    #ghost order: 'Blinky', 'Pinky', 'Inky', 'Clyde'

    #Test
    #pacman_policy = agents.keyboard_controller #use the arrow keys to control pacman
    #ghost_policies = [agents.random_walk for _ in range(4)] 
    #frightened_ghost_policies = [agents.random_walk for _ in range(4)]
    #game_engine.main(pacman_policy, ghost_policies, frightened_ghost_policies, map_file='maps/originalClassic.txt')#map_file = "small-single-ghost.txt")

    #---TP3---
    n_experiments = 30
    search_algorithms = ['bfs', 'dfs', 'greedy', 'a_star']
    #search_algorithms = ['dfs','greedy', 'bfs', 'a_star']
    seed = 42
    all_results = []
    ghost_results = [] # list to store ghost path lengths, no path found rate, stationary rate and moving rate for each ghost and each search algorithm for later analysis and plotting
    for search_algorithm in search_algorithms:
        success_rate =0
        scores = []
        ghost_results = [] # list to store ghost path lengths, no path found rate, stationary rate and moving rate for each ghost and each search algorithm for later analysis and plotting
        print('---search_algorithm: ', search_algorithm,'---')
        
        for experiment in range(n_experiments):
            random.seed(seed + experiment)
            print(f"Experiment {experiment+1}/{n_experiments} with search_algorithm: {search_algorithm} seed: {seed + experiment}")
            pacman_policy = agents.pacman_reactive_agent
            ghost_policies = [agents.blinky_search_agent(search_algorithm), agents.pinky_search_agent(search_algorithm), agents.inky_search_agent(search_algorithm), agents.clyde_search_agent(search_algorithm)]
            #ghost_policies = [agents.inky_search_agent(search_algorithm)]
            frightened_ghost_policies = [agents.run_away_from_pacman_search(search_algorithm) for _ in range(4)]
            #frightened_ghost_policies = [agents.run_away_from_pacman_search(search_algorithm) for _ in range(1)]
            game_state, won = game_engine.main(pacman_policy, ghost_policies, frightened_ghost_policies, map_file='maps/originalClassic.txt')

            if won:
                success_rate += 1

            for ghost in game_state['ghosts']:
                print(ghost['name'], 'mean path lengths: ', np.mean(ghost['path_lengths']), 'no path found rate: ', ghost['no_path_found']/game_state['time_step'], 'stationary rate: ', ghost['stationary']/game_state['time_step'], 'moving rate: ', ghost['moving']/game_state['time_step'])
                # store the ghost path lengths, no path found rate, stationary rate and moving rate in a list for each ghost and each search algorithm for later analysis and plotting also store the search algorithm used for each ghost
                ghost_results.append((ghost['name'], search_algorithm, np.mean(ghost['path_lengths']), ghost['no_path_found']/game_state['time_step'], ghost['stationary']/game_state['time_step'], ghost['moving']/game_state['time_step']))

            scores.append(game_state['score'])      

        # after all experiments print ghost path lengths, no path found rate, stationary rate and moving rate for each ghost and each search algorithm and store the average score, success rate and search algorithm in a list for later analysis and plotting
        print('---search_algorithm: ', search_algorithm,'---')
        for ghost in ['Blinky', 'Pinky', 'Inky', 'Clyde']:
            ghost_data = [result for result in ghost_results if result[0] == ghost and result[1] == search_algorithm]
            mean_path_length = np.mean([result[2] for result in ghost_data])
            no_path_found_rate = np.mean([result[3] for result in ghost_data])
            stationary_rate = np.mean([result[4] for result in ghost_data])
            moving_rate = np.mean([result[5] for result in ghost_data])
            print(ghost, 'mean path lengths: ', mean_path_length, 'no path found rate: ', no_path_found_rate, 'stationary rate: ', stationary_rate, 'moving rate: ', moving_rate)  

        print(f"Average score of {n_experiments} experiments: ", np.mean(scores), 'wins: ', success_rate, 'success rate: ', success_rate/n_experiments*100, '%')
        all_results.append((search_algorithm, ghost_results, np.mean(scores), success_rate, success_rate/n_experiments*100, '%'))

    # Print summary of results
    print("\nSummary of results:")
    for result in all_results:
        print(f"Search Algorithm: {result[0]}, Average Score: {result[2]}, Wins: {result[3]}, Success Rate: {result[4]}")
    # Print ghost results summary
    print("\nGhost results summary:")
    for ghost in ['Blinky', 'Pinky', 'Inky', 'Clyde']:
        print(f"\n{ghost} results:")
        for result in all_results:  
            ghost_data = [res for res in result[1] if res[0] == ghost and res[1] == result[0]]
            mean_path_length = np.mean([res[2] for res in ghost_data])
            no_path_found_rate = np.mean([res[3] for res in ghost_data])
            stationary_rate = np.mean([res[4] for res in ghost_data])
            moving_rate = np.mean([res[5] for res in ghost_data])
            print(f"Search Algorithm: {result[0]}, Mean Path Length: {mean_path_length}, No Path Found Rate: {no_path_found_rate}, Stationary Rate: {stationary_rate}, Moving Rate: {moving_rate}")