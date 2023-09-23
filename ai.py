import WumpusWorld
import numpy

pit_probability = numpy.zeros((10,10), dtype=int)
wumpus_probability = numpy.zeros((10,10), dtype=int)
breeze_location = numpy.zeros((10,10), dtype=bool)
stench_location = numpy.zeros((10,10), dtype=bool)


def find__move(game, agent_position, visited_locations):
    percepts = []
    percepts = game.get_percepts()
    row,col  = agent_position
    if "Breeze" in percepts:
        breeze_location[row,col] = True
        if visited_locations[row+1,col] == False:
            pit_probability[row,col] += 1
        if visited_locations[row-1,col] == False:
            pit_probability[row,col] += 1
        if visited_locations[row,col+1] == False:
            pit_probability[row,col] += 1
        if visited_locations[row,col-1] == False:
            pit_probability[row,col] += 1
    
    if "Stench" in percepts:
        stench_location[row,col] = True
        if visited_locations[row+1,col] == False:
            wumpus_probability[row,col] += 1
        if visited_locations[row-1,col] == False:
            wumpus_probability[row,col] += 1
        if visited_locations[row,col+1] == False:
            wumpus_probability[row,col] += 1
        if visited_locations[row,col-1] == False:
            wumpus_probability[row,col] += 1
    
    return next_move()

def next_move():
    pass


def does_pit_exist(location):
    if pit_probability[location[0],location[1]] > 2:
        return True
    else:
        return False
    
def does_wumpus_exist(location):
    if wumpus_probability[location[0],location[1]] > 2:
        return True
    else:
        return False

def kill_wumpus():
    pass
    # wumpus_probability re 0 kore dite hbe, stench er matrix update hobe
    