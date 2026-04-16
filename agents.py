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

def move_in_path(agent, game_state, path, search_algorithm):
    #This function is called by the search agents to move the agent with the first step in the path

    if path is not None and len(path) > 0:
        next_step = path.pop(0) # pop is used to remove the first element of the list and return it

        if(search_algorithm == 'dfs'):
            # Create a new variable for the next step to move to, and check if it is a valid move before moving the agent.
            # This is to avoid moving the agent in an invalid direction, which can happen with DFS if the path contains 
            # loops or backtracking, leading to errors in the game engine and unrealistic ghost behavior.
            valid_moves = game_engine.get_valid_directions((agent['x'], agent['y']), game_state['grid'], game_state['grid_size'])
            move_direction = None
            if next_step[0] > agent['x']:
                move_direction = 'right'
            elif next_step[0] < agent['x']:
                move_direction = 'left'
            elif next_step[1] > agent['y']: 
                move_direction = 'down'
            elif next_step[1] < agent['y']:
                move_direction = 'up'   

            #remove opposite direction of current direction from valid moves to avoid going back and forth, which can happen with DFS and lead to longer paths and more time spent in the search
            if agent['direction'] is not None and game_engine.opposite_direction(agent['direction']) in valid_moves:
                # dont remove opposite direction if it is the only valid move, otherwise the agent can get stuck in a corner with no valid moves and the game engine will throw an error
                if len(valid_moves) > 1:  
                    valid_moves.remove(game_engine.opposite_direction(agent['direction']))
                    #print("Removed opposite direction", game_engine.opposite_direction(agent['direction']), "from valid moves to avoid going back and forth. Valid moves now: ", valid_moves)

            if move_direction not in valid_moves:
                #print("Next step in path is not a valid move for the agent, skipping move. Next step: ", next_step, "Valid moves: ", valid_moves, "move direction: ", move_direction)
                game_engine.set_direction(agent, game_state, valid_moves[0]) # if the next step is not a valid move, move in a random valid direction to avoid getting stuck and to add some randomness to the ghost's behavior
            else:
                # now actually move the agent in the direction of the next step in the path
                #print("Moving agent in direction: ", move_direction, " towards next step: ", next_step)
                game_engine.set_direction(agent, game_state, move_direction)        
        else:
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
    #"print("BFS: Computing path from", start, "to", goal)
    if start == goal:
        return []

    # first initialize the queue with the start position, and a visited set to keep track of visited nodes, 
    # and a parent dictionary to reconstruct the path once we reach the goal
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        # pop the first position from the queue and check if it is the goal, if it is then reconstruct the path using the parent dictionary and return it
        current = queue.popleft()
        # if it is not the goal, then add its unvisited neighbours to the queue and mark them as visited, and set their parent to the current position
        for neighbour in transition_graph.get(current, []):
            # if the neighbour has already been visited, then skip it to avoid infinite loops and redundant processing
            if neighbour in visited:
                continue
            
            # now add the neighbour to the visited set and the queue, and set its parent to the current position
            visited.add(neighbour)
            parent[neighbour] = current

            # if the neighbour is the goal, then reconstruct the path using the parent dictionary and return it. The path should be a list of 
            # positions from start to goal, excluding the start position so move_in_path can consume the next step.
            if neighbour == goal:
                path = []
                node = goal
                # reconstruct the path by following the parent pointers from the goal back to the start, and then reverse it to get the path from start to goal
                while node != start:
                    path.append(node)
                    node = parent[node]
                # reverse the path to get the correct order from start to goal, and return it
                path.reverse()
                return path

            queue.append(neighbour)

    return None

def depth_first_search(start, goal, transition_graph):
    #TODO: Implement the depth-first search algorithm. It should return the path as a list of positions
    # Hint: you can use a stack (LIFO) data structure to implement the DFS. You can use a list and append/pop
    #  from the end to implement the stack. You should also keep track of visited nodes to avoid infinite loops. 

    #print("DFS: Computing path from", start, "to", goal)
    if start == goal:
        return []

    # first initialize the stack with the start position, and a visited set to keep track of visited nodes,
    stack = [start]
    visited = {start}
    parent = {start: None}

    #print("DFS: entering stack", start, "to", goal)
    while stack:
        # pop the last position from the stack and check if it is the goal, if it is then reconstruct the path using the parent dictionary and return it
        current = stack.pop()
        # if it is not the goal, then add its unvisited neighbours to the stack and mark them as visited, and set their parent to the current position
        for neighbour in transition_graph.get(current, []):
            if neighbour in visited:
                continue

            # check if neighbour is already in stack, if it is then we don't add it again, to 
            # avoid duplicates in the stack which can lead to longer paths and more time spent in the search
            #if neighbour in stack:
            #    print("DFS: neighbour", neighbour, "already in stack, skipping")
            #    continue

            visited.add(neighbour)
            parent[neighbour] = current

            # if the neighbour is the goal, then reconstruct the path using the parent dictionary and return it. The path should be a list of
            if neighbour == goal:
                path = []
                node = goal
                # reconstruct the path by following the parent pointers from the goal back to the start, and then reverse it to get the path from start to goal
                while node != start:
                    path.append(node)
                    node = parent[node]
                path.reverse()
                #print("DFS: path found from", start, "to", goal, ":", path)
                return path
            
            stack.append(neighbour)

    #print("DFS: No path found from", start, "to", goal)
    return None

def greedy_search(start, goal, transition_graph):
    #TODO: Implement the greedy search algorithm. It should return the path as a list of positions
    # use a priority queue data structure to implement the greedy search. 
    # use the heapq library in Python to implement the priority queue. 
    # The priority should be based on the heuristic function, which in this case can be the Manhattan distance 
    # from the current node to the goal. Also keep track of visited nodes to avoid infinite loops.
    if start == goal:
        return []
    
    import heapq
    # the heap will store tuples of (priority, position), where priority is the Manhattan distance from the position to the goal. The heap is initialized with the 
    # start position and its priority, which is the Manhattan distance from the start
    heap = [(game_engine.manhattan_distance(start, goal), start)]
    visited = {start}
    parent = {start: None}

    while heap:
        # pop the position with the lowest priority (the one estimated to be closest to the goal based on the heuristic function) from the heap 
        # and check if it is the goal, if it is then reconstruct the path using the parent dictionary and return it
        _, current = heapq.heappop(heap)
        for neighbour in transition_graph.get(current, []):
            if neighbour in visited:
                continue

            visited.add(neighbour)
            parent[neighbour] = current

            # if the neighbour is the goal, then reconstruct the path using the parent dictionary and return it. The path should be a list of positions 
            # from start to goal, excluding the start position so move_in_path can consume the next step.
            if neighbour == goal:
                path = []
                node = goal
                while node != start:
                    path.append(node)
                    node = parent[node]
                # reverse the path to get the correct order from start to goal, and return it
                path.reverse()
                return path
            # the priority is based on the heuristic function, which in this case can be the Manhattan distance from the current node to the goal. the prioirity queue is sorted
            #  by the priority, so the node with the lowest priority will be popped first, which is the node that is estimated to be closest to the goal based on the 
            # heuristic function. In case of ties in the priority, the node that was added to the heap first will be popped first, which can lead to different 
            # paths being explored and can affect the performance of the algorithm.
            heapq.heappush(heap, (game_engine.manhattan_distance(neighbour, goal), neighbour))

    return None

def a_star_search(start, goal, transition_graph):
    #TODO: Implement the A* search algorithm. It should return the path as a list of positions
    # use a priority queue data structure to implement the A* search. 
    # use the heapq library in Python to implement the priority queue. 
    # The priority should be based on the cost function, which is the sum of the path cost from the start node to the 
    # current node and the heuristic function, which in this case will be the Manhattan distance from the current node to the goal. 
    # Also keep track of visited nodes to avoid infinite loops.
    if start == goal:
        return []
    
    import heapq

    # the heap will store tuples of (priority, cost, position), where priority is the sum of the path cost from the start node to the current node and the
    #  heuristic function, which in this case will be the Manhattan distance from the current node to the goal. The heap is initialized with the start position, 
    # its priority, which is the Manhattan distance from the start, and its cost, which is 0.
    heap = [(0 + game_engine.manhattan_distance(start, goal), 0, start)]
    visited = {start: 0}
    parent = {start: None}  

    while heap:
        # pop the position with the lowest priority (the one estimated to be closest to the goal based on the heuristic function and the path cost) from the heap 
        # and check if it is the goal, if it is then reconstruct the path using the parent dictionary and return it .
        _, cost, current = heapq.heappop(heap)
        if current == goal:
            path = []
            node = goal
            while node != start:
                path.append(node)
                node = parent[node]
            # reverse the path to get the correct order from start to goal, and return it
            path.reverse()
            return path

        for neighbour in transition_graph.get(current, []):
            new_cost = cost + 1  # assuming uniform cost for each step
            if neighbour in visited and visited[neighbour] <= new_cost:
                continue

            visited[neighbour] = new_cost
            parent[neighbour] = current
            # the priority is the sum of the path cost from the start node to the current node and the heuristic function, which in this case will be the Manhattan distance 
            # from the current node to the goal. the prioirity queue is sorted by the priority, so the node with the lowest priority will be popped first, 
            # which is the node that is estimated to be closest to the goal based on the heuristic function and the path cost. In case of ties in the priority,
            # the node that was added to the heap first will be popped first, which can lead to different paths being explored and can affect the performance of the algorithm.
            heapq.heappush(heap, (new_cost + game_engine.manhattan_distance(neighbour, goal), new_cost, neighbour))

    return None


def blinky_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #TODO: Implement the search agent for Blinky
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        pacman = game_state['pacman']
        goal = (pacman['x'], pacman['y'])
        #print("Blinky: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)
        #print("Blinky: Path found from", start, "to", goal, ":", path)
        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path, search_algorithm)

        current_pos = (ghost['x'], ghost['y'])
        #print("Blinky: Current position after moving in path:", current_pos)
    return agent


def pinky_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        pacman = game_state['pacman']
        # find all positions in the transition graph that are within 4 steps of pacman, and choose the one that is 
        # closest to pinky as the goal. This will make pinky try to cut off pacman by targeting a position in front of him, 
        # rather than directly targeting pacman's current position like blinky.
        all_positions = list(game_state['transition_graph'].keys())
        positions_with_distance = [(pos, game_engine.manhattan_distance(pos, (pacman['x'], pacman['y']))) for pos in all_positions]
        positions_with_distance = [pd for pd in positions_with_distance if pd[1] <= 4]
        
        goal = min(positions_with_distance, key=lambda pd: game_engine.manhattan_distance(pd[0], start))[0] 

        #goal = (pacman['x'], pacman['y'])
        #print("Pinky: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)

        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path, search_algorithm)
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

        #print("Inky: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)

        # store goal and path in ghost's state for debugging and analysis purposes
        ghost['current_goal'] = goal
        ghost['current_path'] = path
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path, search_algorithm)
    return agent


def clyde_search_agent(search_algorithm):
    def agent(ghost, game_state):
        #TODO: Implement the search agent for Clyde
        #1.Define the start and goal positions (as tuples of x,y)
        start = (ghost['x'], ghost['y'])
        pacman = game_state['pacman']
        # if distance to pacman is greater than 5 then goal is pacman's position, else goal 
        # is a random position in the transition graph, to add some randomness to Clyde's behaviour and differentiate it from the other ghosts, which will always target pacman's current position. This is a simple way to add some unpredictability to Clyde's behaviour, which can be turned on or off by changing the definition of the goal.
        distance_to_pacman = game_engine.manhattan_distance(start, (pacman['x'], pacman['y']))
        if distance_to_pacman > 5:
            goal = (pacman['x'], pacman['y'])
        else:
            goal = random.choice(list(game_state['transition_graph'].keys()))

        #print("Clyde: Computing path from", start, "to", goal)

        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path, search_algorithm)
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
        #print("Run away: Computing path from", start, "to", goal)
        #2.Use the compute_path function to compute the path from start to goal. The transition graph is already computed and is accessible in game_state['transition_graph']   
  
        path = compute_path(start, goal, game_state['transition_graph'], search_algorithm, ghost)
        #3.Use the move_in_path function to move the ghost in the first step of the path
        move_in_path(ghost, game_state, path, search_algorithm)
        
    return agent
