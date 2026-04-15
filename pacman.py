import game_engine
import agents
import numpy as np
import matplotlib.pyplot as plt

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

    for search_algorithm in search_algorithms:
        success_rate =0
        scores = []
        print('---search_algorithm: ', search_algorithm,'---')
        
        for experiment in range(n_experiments):
            
            pacman_policy = agents.pacman_reactive_agent
            ghost_policies = [agents.blinky_search_agent(search_algorithm), agents.pinky_search_agent(search_algorithm), agents.inky_search_agent(search_algorithm), agents.clyde_search_agent(search_algorithm)]
            frightened_ghost_policies = [agents.run_away_from_pacman_search(search_algorithm) for _ in range(4)]
            game_state = game_engine.main(pacman_policy, ghost_policies, frightened_ghost_policies, map_file='maps/originalClassic.txt')

            
            for ghost in game_state['ghosts']:
                print(ghost['name'], 'mean path lengths: ', np.mean(ghost['path_lengths']), 'no path found rate: ', ghost['no_path_found']/game_state['time_step'], 'stationary rate: ', ghost['stationary']/game_state['time_step'], 'moving rate: ', ghost['moving']/game_state['time_step'])
            
            scores.append(game_state['score'])      
                
        print(f"Average score of {n_experiments} experiments: ", np.mean(scores), 'success rate: ', success_rate/n_experiments)
