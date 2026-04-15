import game_engine
import random
def ghost_up(game_state, range=1):
    pacman = game_state['pacman']
        
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['y'] - visibility < 0 or game_state['grid'][pacman['y'] - visibility][pacman['x']] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['y'] == pacman['y'] - visibility and ghost['x'] == pacman['x']:
                    return True
                    
            visibility += 1
    return False

def ghost_down(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['y'] + visibility >= game_state['grid_size'][1] or game_state['grid'][pacman['y'] + visibility][pacman['x']] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['y'] == pacman['y'] + visibility and ghost['x'] == pacman['x']:
                    return True

            visibility += 1
    return False

def ghost_left(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['x'] - visibility < 0 or game_state['grid'][pacman['y']][pacman['x'] - visibility] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['y'] == pacman['y']  and ghost['x'] == pacman['x']- visibility:
                    return True
            visibility += 1
    return False

def ghost_right(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['x'] + visibility >= game_state['grid_size'][0] or game_state['grid'][pacman['y']][pacman['x'] + visibility] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['y'] == pacman['y']  and ghost['x'] == pacman['x'] + visibility:
                    return True
            visibility += 1
    return False


def dot_up(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['y'] - visibility < 0 or game_state['grid'][pacman['y'] - visibility][pacman['x']] == game_engine.WALL:
            break
        else:
            if game_state['grid'][pacman['y']-visibility][pacman['x']] == game_engine.DOT or game_state['grid'][pacman['y']-visibility][pacman['x']] == game_engine.POWER_PELLET:
                return True
            visibility += 1
    return False
    
def dot_down(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['y'] + visibility >= game_state['grid_size'][1] or game_state['grid'][pacman['y'] + visibility][pacman['x']] == game_engine.WALL:
            break
        else:
            if game_state['grid'][pacman['y']+visibility][pacman['x']] == game_engine.DOT or game_state['grid'][pacman['y']+visibility][pacman['x']] == game_engine.POWER_PELLET:
                return True
            visibility += 1
    return False


    
def dot_left(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['x'] - visibility < 0 or game_state['grid'][pacman['y']][pacman['x'] - visibility] == game_engine.WALL:
            break
        else:
            if game_state['grid'][pacman['y']][pacman['x'] - visibility] == game_engine.DOT or game_state['grid'][pacman['y']][pacman['x'] - visibility] == game_engine.POWER_PELLET:
                return True
            visibility += 1
    return False
    
    
def dot_right(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['x'] + visibility >= game_state['grid_size'][0] or game_state['grid'][pacman['y']][pacman['x'] + visibility] == game_engine.WALL:
            break
        else:
            if game_state['grid'][pacman['y']][pacman['x'] + visibility] == game_engine.DOT or game_state['grid'][pacman['y']][pacman['x'] + visibility] == game_engine.POWER_PELLET:
                return True
            visibility += 1
    return False

def ghost_frightened_up(game_state, range=1):
    pacman = game_state['pacman']
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['y'] - visibility < 0 or game_state['grid'][pacman['y'] - visibility][pacman['x']] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['scared'] and ghost['y'] == pacman['y'] - visibility and ghost['x'] == pacman['x']:
                    return True
            visibility += 1
    return False

def ghost_frightened_down(game_state, range=1):
    pacman = game_state['pacman']
        
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['y'] + visibility >= game_state['grid_size'][1] or game_state['grid'][pacman['y'] + visibility][pacman['x']] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['scared'] and ghost['y'] == pacman['y'] + visibility and ghost['x'] == pacman['x']:
                    return True

            visibility += 1
    return False

def ghost_frightened_left(game_state, range=1):
    pacman = game_state['pacman']
    
    
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['x'] - visibility < 0 or game_state['grid'][pacman['y']][pacman['x'] - visibility] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['scared'] and ghost['y'] == pacman['y']  and ghost['x'] == pacman['x']- visibility:
                    return True
            visibility += 1
    return False

def ghost_frightened_right(game_state, range=1):
    pacman = game_state['pacman']
        
    visibility = 0
    while(visibility < range):
        ##check how far we can see. This is limited by both range and walls
        if pacman['x'] + visibility >= game_state['grid_size'][0] or game_state['grid'][pacman['y']][pacman['x'] + visibility] == game_engine.WALL:
            break
        else:
            for ghost in game_state['ghosts']:
                if ghost['alive'] and ghost['scared'] and ghost['y'] == pacman['y']  and ghost['x'] == pacman['x'] + visibility:
                    return True
            visibility += 1
    return False

def wall_up(game_state):
    pacman = game_state['pacman']
    
    if pacman['y'] == 0 or game_state['grid'][pacman['y'] - 1][pacman['x']] == game_engine.WALL:
        return True
    return False

def wall_down(game_state):
    pacman = game_state['pacman']
    
    if pacman['y'] == game_state['grid_size'][1]-1 or game_state['grid'][pacman['y'] + 1][pacman['x']] == game_engine.WALL:
        return True
    return False

def wall_left(game_state):
    pacman = game_state['pacman']
    
    if pacman['x'] == 0 or game_state['grid'][pacman['y']][pacman['x'] - 1] == game_engine.WALL:
        return True
    return False

def wall_right(game_state):
    pacman = game_state['pacman']
    
    if pacman['x'] == game_state['grid_size'][0]-1 or game_state['grid'][pacman['y']][pacman['x'] + 1] == game_engine.WALL:
        return True
    return False

def noisy_ghost_position_sensor(game_state, ind_ghost, prob):
    if random.random()<prob:
        return (game_state['ghosts'][ind_ghost]['x'], game_state['ghosts'][ind_ghost]['y'])
    else:
        candidates = []
        for x in range(game_state['ghosts'][ind_ghost]['x']-1, game_state['ghosts'][ind_ghost]['x']+2):
            for y in range(game_state['ghosts'][ind_ghost]['y']-1, game_state['ghosts'][ind_ghost]['y']+2):
                
                if (x,y) != (game_state['ghosts'][ind_ghost]['x'], game_state['ghosts'][ind_ghost]['y']) and x>=0 and x<len(game_state['grid'][0]) and y>=0 and y<len(game_state['grid']) and game_state['grid'][y][x] != game_engine.WALL:
                    candidates.append((x,y))
        return random.choice(candidates)
