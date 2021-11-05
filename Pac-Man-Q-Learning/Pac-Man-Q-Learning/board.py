import numpy as np

class Board:
    def __init__(self):
        self.grid = np.loadtxt('board.txt', dtype=int)
        self.score = 0
        self.ghosts = []

    def add_ghost(self, ghost):
        self.ghosts.append(ghost)

    def is_intersection(self, x, y):
        possible_actions = self.possible_actions(x, y)

        # if we can change direction we are at an intersection
        return ("RIGHT" in possible_actions or "LEFT" in possible_actions) and ("UP" in possible_actions or "DOWN" in possible_actions)
    
    # determine if action is possible based on surrounding walls/maze boundaries
    def possible_actions(self, x, y):
        possible_actions = []
        if (y-1) >= 0 and self.grid[y-1][x] != 0:
            possible_actions.append("UP")
        if (y+1) < len(self.grid) and self.grid[y+1][x] != 0:
            possible_actions.append("DOWN")
        if (x-1) >= 0 and self.grid[y][x-1] != 0:
            possible_actions.append("LEFT")
        if (x+1) < len(self.grid[y]) and self.grid[y][x+1] != 0:
            possible_actions.append("RIGHT")
        return possible_actions

    # get reward from grid contents and update
    def get_reward(self, agent):
        value = self.grid[agent.y][agent.x]
        reward = 0
        if value == 1:
            reward = 1
            self.grid[agent.y][agent.x] = 4
            agent.pills_eaten += 1
            agent.score += 50
        elif value == 2:
            reward = 20
            self.grid[agent.y][agent.x] = 4
            agent.pills_eaten += 1
            agent.score += 100
        elif value == 4:
            reward = -1

        return reward

    def breadth_first_search(self, action, x, y):
        distances = []

        return distances