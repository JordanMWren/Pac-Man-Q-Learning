from board import Board
from characters import *
from episode import Episode
from case import Case

# define our learning rate, discount factor, and similarity function weights
Episode.alpha = .1
Episode.gamma = .98
Case.weight_pills = .2
Case.weight_power_pills = .05
Case.weight_ghosts = .7
Case.weight_edible_ghosts = .05

# define our initial case to hold "FAR" in every value
initial_case = Case()
initial_case.distance_pills = ["FAR"] * 4
initial_case.distance_powerpill = ["FAR"] * 4
initial_case.distance_inedible_ghost = ["FAR"] * 4
initial_case.distance_edible_ghost = ["FAR"] * 4

# initialize the q table and case base and begin simulating episodes
qtable = [[0] * 4]
case_base = [initial_case]
for i in range(500):
    episode = Episode()
    episode.simulate(qtable, case_base)