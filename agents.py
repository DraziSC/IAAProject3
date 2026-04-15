import game_engine
import pygame
import pacman_perceptions
import random
import numpy as np
import actions
from collections import deque

def keyboard_controller(game_state):
    direction = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state['running'] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = 'up'
            elif event.key == pygame.K_DOWN:
                direction = 'down'
            elif event.key == pygame.K_LEFT:
                direction = 'left'
            elif event.key == pygame.K_RIGHT:
                direction = 'right'
                
    pacman = game_state['pacman']
    grid = game_state['grid']
    grid_size = game_state['grid_size']
        
    if (direction is None and not game_engine.PACMAN_CONTINUOUS_MOTION) or direction in game_engine.get_valid_directions((pacman['x'],pacman['y']), grid, grid_size):
        pacman['previous_direction'] = pacman['direction']
        pacman['direction'] = direction
            
    elif direction is not None and direction not in game_engine.get_valid_directions((pacman['x'],pacman['y']), grid, grid_size):
        #pacman['previous_direction'] = pacman['direction']
        pacman['next_direction'] = direction
        
    elif direction is None and game_engine.PACMAN_CONTINUOUS_MOTION and pacman['next_direction'] in game_engine.get_valid_directions((pacman['x'],pacman['y']), grid, grid_size):
        pacman['previous_direction'] = pacman['direction']

        pacman['direction'] = pacman['next_direction']
        pacman['next_direction'] = None
        
def random_walk(agent, game_state):
    grid = game_state['grid']
    grid_size = game_state['grid_size']
    directions = game_engine.get_valid_directions((agent['x'],agent['y']), grid, grid_size)
    if len(directions)>1 and agent['direction'] is not None and game_engine.opposite_direction(agent['direction']) in directions:
        directions.remove(game_engine.opposite_direction(agent['direction']))

    agent['direction'] = random.choice(directions)
    

def stationary_agent(ghost, game_state):
    pass
    
def pacman_reactive_agent(game_state):
    pacman = game_state['pacman']
    grid = game_state['grid']
    grid_size = game_state['grid_size']
    
    directions = game_engine.get_valid_directions((pacman['x'],pacman['y']), grid, grid_size)    
        
    for dir in directions:
        if eval('pacman_perceptions.ghost_'+dir)(game_state, range=game_engine.PACMAN_GHOST_RANGE):
            if eval('pacman_perceptions.ghost_frightened_'+dir)(game_state, range=game_engine.PACMAN_GHOST_RANGE):                
                eval('actions.go_'+dir)(pacman, game_state)
                return
            else:
                directions.remove(dir)
            
    
    if len(directions)>1:
        for dir in directions:
            if eval('pacman_perceptions.dot_'+dir)(game_state, range=game_engine.PACMAN_DOT_RANGE):
                eval('actions.go_'+dir)(pacman, game_state)
                return
    
    op = game_engine.opposite_direction(pacman['direction'])
    if len(directions)>1 and op in directions:
        directions.remove(op)
        
    if len(directions) == 0:
        eval('actions.go_'+op)(pacman, game_state)
    else:    
        eval('actions.go_'+random.choice(directions))(pacman, game_state)
        

    
    
def get_neighbours(pos, valid_positions):
    #returns the valid cells (without obstacles) adjacent to the cell s
    valid_neighbours = []
    xs, ys = pos
    for candidate in ((xs-1, ys), (xs+1, ys), (xs, ys-1), (xs, ys+1)):
        if candidate in valid_positions:
            valid_neighbours.append(candidate)
    return valid_neighbours

##---TP3---

def compute_path(start, goal, transition_graph, search_algorithm, agent):
    #This function is called by the search agents to compute the path from start to goal. It is already fully implemented
    path = None
    if search_algorithm == 'bfs':
        path = breadth_first_search(start, goal , transition_graph)
    elif search_algorithm == 'dfs':
        path = depth_first_search(start, goal , transition_graph)
    elif search_algorithm == 'greedy':
        path = greedy_search(start, goal , transition_graph)
    elif search_algorithm == 'a_star':
        path = a_star_search(start, goal , transition_graph)
    else:
        raise ValueError("Unknown search algorithm")

    if path is None:
        agent['no_path_found'] += 1
    elif start == goal:
        agent['stationary'] +=1
    else:
        agent['moving'] +=1                
        agent['path_lengths'].append(len(path))
    
    return path

def move_in_path(agent, game_state, path):
    #This function is called by the search agents to move the agent with the first step in the path

    if path is not None and len(path) > 0:
        next_step = path.pop(0) # pop is used to remove the first element of the list and return it

        if next_step[0] > agent['x']:
            actions.go_right(agent, game_state)
        elif next_step[0] < agent['x']:
            actions.go_left(agent, game_state)
        elif next_step[1] > agent['y']:
            actions.go_down(agent, game_state)
        elif next_step[1] < agent['y']:
            actions.go_up(agent, game_state)


def breadth_first_search(start, goal, transition_graph):
    # Breadth-first search returning the sequence of positions from start to goal,
    # excluding the start position so move_in_path can consume the next step.
    print("BFS: Computing path from", start, "to", goal)
    if start == goal:
        return []

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        current = queue.popleft()
        for neighbour in transition_graph.get(current, []):
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = current

            if neighbour == goal:
                path = []
                node = goal
                while node != start:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return path

            queue.append(neighbour)

    return None

def depth_first_search(start, goal, transition_graph):
    #TODO: Implement the depth-first search algorithm. It should return the path as a list of positions
    # Hint: you can use a stack (LIFO) data structure to implement the DFS. You can use a list and append/pop
    #  from the end to implement the stack. You should also keep track of visited nodes to avoid infinite loops. 

    if start == goal:
        return []

    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        current = stack.pop()
        for neighbour in transition_graph.get(current, []):
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = current

            if neighbour == goal:
                path = []
                node = goal
                while node != start:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                return path

            stack.append(neighbour)

    return None

def greedy_search(start, goal, transition_graph):
    #TODO: Implement the greedy search algorithm. It should return the path as a list of positions
    #
    return None

def a_star_search(start, goal, transition_graph):
    #TODO: Implement the A* search algorithm. It should return the path as a list of positions
    return None


def blinky_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #TODO: Implement the search agent for Blinky
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        pacman = game_state['pacman']
        goal = (pacman['x'], pacman['y'])
        print("Blinky: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)
        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path)
    return agent


def pinky_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        pacman = game_state['pacman']
        goal = (pacman['x'], pacman['y'])
        print("Pinky: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)

        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path)
    return agent

def inky_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #TODO: Implement the search agent for Inky
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        # Goal will be a random position in the transition graph, to add some randomness to Inky's behaviour and differentiate it from Blinky and Pinky, which will always target pacman's current position. This is a simple way to add some unpredictability to Inky's behaviour, which can be turned on or off by changing the definition of the goal.
        # if goal is equal to start then pick a new random

        current_goal = ghost.get('current_goal')
        if current_goal is not None and current_goal != start:
            goal = current_goal
        else:
            goal = random.choice(list(game_state['transition_graph'].keys()))

        print("Inky: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)

        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path)
    return agent


def clyde_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #TODO: Implement the search agent for Clyde
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        pacman = game_state['pacman']
        goal = (pacman['x'], pacman['y'])
        print("Clyde: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path)
        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
    return agent
    
    
def run_away_from_pacman_search(search_algorithm):
    def agent(ghost, game_state):
        #TODO: Implement the search agent for running away from pacman (used by all the ghosts in the frightened state)

        #1.Define the start and goal positions (as tuples of x,y
        # start is the current position of the ghost
        start = (ghost['x'], ghost['y'])
        # Goal will be further distance from pacman, so we can define it as the position in the transition graph 
        # that is furthest from pacman, which we can find by iterating over all the positions in the transition graph 
        # and computing their distance to pacman, and taking the one with the maximum distance. This is a simple way to 
        # define a goal for running away from pacman.
        pacman = game_state['pacman']
        max_distance = -1
        goal = start
        for pos in game_state['transition_graph'].keys():
            distance = pacman_perceptions.pacman_distance_to_position(game_state, pos)
            if distance > max_distance:
                max_distance = distance
                goal = pos
        print("Run away: Computing path from", start, "to", goal)
        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
  
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path)
        
    return agent
