import numpy as np

class Board:
    def __init__(self):
        self.grid = np.loadtxt('board.txt', dtype=str)
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
        if self.grid[y-1][x] != '0' and self.grid[y-1][x] != '-':
            possible_actions.append("UP")
        if self.grid[y+1][x] != '0' and self.grid[y+1][x] != '-':
            possible_actions.append("DOWN")
        if self.grid[y][x-1] != '0' and self.grid[y][x-1] != '-':
            possible_actions.append("LEFT")
        if self.grid[y][x+1] != '0' and self.grid[y][x+1] != '-':
            possible_actions.append("RIGHT")

        return possible_actions

    # get reward from grid contents and update
    def get_reward(self, agent):
        value = int(self.grid[agent.y, agent.x])
        if value == 1:
            agent.pills_eaten += 1
            agent.score += 50
        elif value == 50:
            agent.pills_eaten += 1
            agent.score += 100
        
        self.grid[agent.y, agent.x] = "-1"
        return value

    def breadth_first_search(self, action, x, y):
        distances = {}
        visited_coords = [(x,y)]

        if action == "UP":
            y -= 1
        elif action == "DOWN":
            y += 1
        elif action == "LEFT":
            x -= 1
        elif action == "RIGHT":
            x += 1

        spaces = []
        spaces.append([x,y])
        distance = 1
        while len(distances) < 3:
            new_spaces = []
            for space in spaces:
                coords = (space[0], space[1])
                if coords in visited_coords:
                    continue
                
                # add the current coordinates to visited coordinates so we don't back-track during search
                visited_coords.append(coords)
                item = self.num_to_value(coords[0], coords[1])
                if item != "none":
                    if item not in distances:
                        distances[item] = distance
                
                # if there's a ghost in this space and it's the first one, we want to add it to our distances
                for ghost in self.ghosts:
                    ghost_coords = (ghost.x, ghost.y)
                    if ghost.edible == False:
                        feature = "ghost"
                    else:
                        feature = "edible_ghost"
                    
                    if ghost_coords == coords and feature not in distances:
                        distances[feature] = distance

                # find all possible directions from current space and add them to next level of search
                possible_actions = self.possible_actions(coords[0], coords[1])
                
                if "UP" in possible_actions:
                    new_spaces.append((coords[0], coords[1] - 1))
                if "DOWN" in possible_actions:
                    new_spaces.append((coords[0], coords[1] + 1))
                if "LEFT" in possible_actions:
                    new_spaces.append((coords[0] - 1, coords[1]))
                if "RIGHT" in possible_actions:
                    new_spaces.append((coords[0] + 1, coords[1]))
            
            spaces = new_spaces
            
            distance += 1
            if distance >= 60:
                break

        # convert distance into a discrete value
        for key in distances:
            distances[key] = self.discrete_distance(distances[key])
        
        if "edible_ghost" not in distances:
            distances["edible_ghost"] = "FAR"
        elif "ghost" not in distances:
            distances["ghost"] = "FAR"

        return distances

    def num_to_value(self, x, y):
        val = "none"
        if self.grid[y][x] == "1":
            val = "pill"
        elif self.grid[y][x] == "50":
            val = "powerpill"
        
        return val

    def discrete_distance(self, distance):
        if distance >= 57:
            distance = "FAR"
        elif distance >= 13:
            distance = "MEDIUM"
        elif distance >= 4:
            distance = "CLOSE"
        else:
            distance = "VERY CLOSE"
        
        return distance