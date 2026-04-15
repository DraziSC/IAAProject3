import game_engine

def go_up(agent, game_state):
    game_engine.set_direction(agent, game_state, 'up')

def go_down(agent, game_state):
    game_engine.set_direction(agent, game_state, 'down')

def go_left(agent, game_state):
    game_engine.set_direction(agent, game_state, 'left')
    
def go_right(agent, game_state):
    game_engine.set_direction(agent, game_state, 'right')