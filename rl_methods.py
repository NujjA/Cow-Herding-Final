import numpy as np
import movement_control

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UP_LEFT = 4
UP_RIGHT = 5
DOWN_LEFT = 6
DOWN_RIGHT = 7
STAY = 8

action_space = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT, STAY]

def action_word(action):
    print("action word ", action)
    if action == UP:
        return "UP"
    if action == DOWN:
        return "DOWN"
    if action == LEFT:
        return "LEFT"
    if action == RIGHT:
        return "RIGHT"
    if action == UP_LEFT:
        return "UP_LEFT"
    if action == UP_RIGHT:
        return "UP_RIGHT"
    if action == DOWN_LEFT:
        return "DOWN_LEFT"
    if action == DOWN_RIGHT:
        return "DOWN_RIGHT"
    if action == STAY:
        return "STAY"
        
    return "INVALID ACTION"
    
    
def action_next_location(agent, grid, action):
    #print("in action next location")
    up_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]))
    down_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]))
    left_cell = grid.torus_adj((agent.pos[0], agent.pos[1]-1))
    right_cell = grid.torus_adj((agent.pos[0], agent.pos[1]+1))
    ul_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]-1))
    dl_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]-1))
    ur_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]+1))
    dr_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]+1))
    
    if action == UP:
        return up_cell
    if action == DOWN:
        return down_cell
    if action == RIGHT:
        return right_cell
    if action == LEFT:
        return left_cell
    if action == UP_LEFT:
        return ul_cell
    if action == DOWN_LEFT:
        return dl_cell
    if action == UP_RIGHT:
        return ur_cell
    if action == DOWN_RIGHT:
        return dr_cell
    if action == STAY:
        return agent.pos
        
    print("action next location error: not an available action")
    #if not any of the moving actions, then STAY
    return agent.pos

def possible_action_space(agent):
    grid = agent.model.grid
    #possible_actions = [STAY] # Uncomment if STAY is a viable option
    possible_actions = [] # Uncomment if STAY is not a viable option
    
    up_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]))
    down_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]))
    left_cell = grid.torus_adj((agent.pos[0], agent.pos[1]-1))
    right_cell = grid.torus_adj((agent.pos[0], agent.pos[1]+1))
    ul_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]-1))
    dl_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]-1))
    ur_cell = grid.torus_adj((agent.pos[0]+1, agent.pos[1]+1))
    dr_cell = grid.torus_adj((agent.pos[0]-1, agent.pos[1]+1))
    
    if grid.is_cell_empty(up_cell):
        possible_actions.append(UP)
    if grid.is_cell_empty(down_cell):
        possible_actions.append(DOWN)
    if grid.is_cell_empty(left_cell):
        possible_actions.append(LEFT)
    if grid.is_cell_empty(right_cell):
        possible_actions.append(RIGHT)
    if grid.is_cell_empty(ul_cell):
        possible_actions.append(UP_LEFT)
    if grid.is_cell_empty(dl_cell):
        possible_actions.append(DOWN_LEFT)
    if grid.is_cell_empty(ur_cell):
        possible_actions.append(UP_RIGHT)
    if grid.is_cell_empty(dr_cell):
        possible_actions.append(DOWN_RIGHT)
        
    return possible_actions


def encode_state(grid): 
    
    list_state = np.zeros((grid.width, grid.height))
    for cell in grid.coord_iter():
        cell_content, x, y = cell
        if cell_content:
            #print(cell_content, x, y)
            #state[x][y] = encode_cell(cell_content)
            list_state[y][x] = encode_cell(cell_content) 
    
    state_tuple = [tuple(l) for l in list_state]
    return tuple(state_tuple)
    
def encode_state_range(agent, vision_range) :
    grid = agent.model.grid
    radius = vision_range
    #cell_locations = grid.get_neighborhood(agent.pos, moore = True, include_center = True, radius = vision_range)
    state_w_h = vision_range + vision_range + 1
    list_state = np.zeros((state_w_h, state_w_h))
    list_x = 0 #stored in list as
    list_y = 0 #stored in list as
    pos_x = agent.pos[0] # actual location of agent to start
    pos_y = agent.pos[1] # actual location of agent to start
    for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                
                grid_position = grid.torus_adj((pos_x + dx, pos_y + dy))
                if not grid.is_cell_empty(grid_position):
                    # get cell content of grid position
                    cell_content = grid[grid_position[0]][grid_position[1]]
                    list_state[list_x][list_y] = encode_cell(cell_content)
                list_x += 1
            list_y += 1
            list_x = 0
    
    distance = int(round(movement_control.get_distance(grid, agent.pos, agent.model.goalTarget)))
    print("distance is ", distance)
    state_tuple = [tuple(l) for l in list_state]
    #extra_information = (distance, agent.model.current_cow_count)
    extra_information = (pos_x, pos_y)
    #print(tuple([tuple(state_tuple), extra_information]))
    return tuple([tuple(state_tuple), extra_information])
                
def grid_to_lists(grid): #TODO: Old method, unused
    list_state = np.zeros((grid.width, grid.height))
    for cell in grid.coord_iter():
        cell_content, x, y = cell
        if cell_content:
            #print(cell_content, x, y)
            #state[x][y] = encode_cell(cell_content)
            list_state[y][x] = encode_cell(cell_content) 
    
    return list_state

def encode_cell(cell_item):
    if cell_item.__class__.__name__ is "WallAgent":
        return 1
    if cell_item.__class__.__name__ is "RandomAgent":
        return 2
    if cell_item.__class__.__name__ is "CowAgent":
        return 3
    if cell_item.__class__.__name__ is "PlanAgent":
        return 4
    if cell_item.__class__.__name__ is "MonteCarloAgent":
        return 5
    if cell_item.__class__.__name__ is "TrainedMonteCarloAgent":
        return 5
    if cell_item.__class__.__name__ is "TDAgent":
        return 6

    return 0

def running_mean(x):
    ''' accept a list of numbers x as input. It should return a list mean_values, where mean_values[k] is the mean of x[:k+1].
    Note: Pay careful attention to indexing! Here, x_k corresponds to x[k-1] 
    (so x_1 = x[0], x_2  = x[1], etc).'''
    mu = 0
    mean_values = []
    for k in np.arange(0, len(x)):
        mu = mu + ((1.0/(k+1)) * (x[k] - mu))
        mean_values.append(mu)
    return mean_values
    
def select_action_old(Q, epsilon, possible_actions, num_actions, state):
    ''' choose action based on episilon-greedy method'''
    
    #make a list of probabilities based on episilon greedy policy
    #### fill all actions with default probability
    probabilities = np.ones(num_actions) * epsilon / len(possible_actions)
    
    #### change the non-possible actions to 0
    for action in range(num_actions):
        if action not in possible_actions:
            probabilities[action] = 0        
    
    #### change the max action to the correct probability
    # if a is the max of Q[s][a] 
    max_action = np.argmax(Q[state])
    # change that action's probability 
    probabilities[max_action] = 1 - epsilon + (epsilon / num_actions)

    print("possible actions: ", possible_actions)
    print("probabilities: ", probabilities)
    
    # list of possible choices of actions 
    action_choices = np.arange(num_actions)
    
    print("action choices: ", action_choices)
    print("possible actions: ", possible_actions)
    print("probabilities: ", probabilities)

    # choose one of the actions based on list of probabilities
    action = np.random.choice(action_choices, p = probabilities)
    
    return action
    
    
def select_e_greedy_action(Q, epsilon, possible_actions, state):
    ''' choose action based on episilon-greedy method'''
    
    nA = len(possible_actions)
    
    #make a list of probabilities based on episilon greedy policy
    #### fill all actions with default probability
    probabilities = np.ones(nA) * epsilon / nA
       
    #### change the max action to the correct probability
    
    #max_action = np.argmax(Q[state]) #argmax gives the first if multiple so dont wan't that
        
    index_list = [-1]
    maxval = -np.inf
    print("Q state is ", Q[state]) 
    for i, s in enumerate (Q[state]):
        if s > maxval:
            maxval = s
            index_list = [i]
        elif s == maxval:
            index_list.append(i)
            
    print("max index list: ", index_list)
    max_action = np.random.choice(i) # if there are multiple max, pick one
    
    print("max_action: ", max_action)
    
    # change that action's probability     
    if max_action in possible_actions:
        # find the index of max_action in possible actions
        index_max = possible_actions.index(max_action)
        print("index max: ", index_max)
        # change the probability of that action
        probabilities[index_max] = 1 - epsilon + (epsilon / nA)
        
        # choose one of the actions based on list of probabilities
        action = np.random.choice(possible_actions, p = probabilities)
    else:
        action = np.random.choice(possible_actions)
        print("max action is not in possible actions, pick a random action from list")

    #print("possible actions: ", possible_actions)
    #print("probabilities: ", probabilities)
    #print("prob sum: ", probabilities.sum())
    print("action: ", action)

    
    
    return action
    
def max_action_with_choice(Q, state, possible_actions):
    print("in max action with choice")
    epsilon = .00001
    return select_e_greedy_action(Q, epsilon, possible_actions, state)
    
