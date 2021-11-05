class Case:
    """
    This class is used to hold the 4 vectors of 4 values to represent the distances
    to the closest of each feature in every direction. This is run through a similarity
    function to help determine which case is the most similar to the current state.
    """
    weight_pills = .25
    weight_power_pills = .25
    weight_ghosts = .25
    weight_edible_ghosts = .25

    def __init__(self):
        self.distance_pills = []
        self.distance_powerpill = []
        self.distance_inedible_ghost = []
        self.distance_edible_ghost = []

    def similarity(self, other_case):
        dist_pills = 0
        dist_powerpills = 0
        dist_inedible_ghosts = 0
        dist_edible_ghosts = 0
        # calculate the distance value between each distance vector
        for i in range(4):
            if other_case.distance_pills[i] == self.distance_pills[i]:
                dist_pills += 1
            if other_case.distance_powerpill[i] == self.distance_powerpill[i]:
                dist_pills += 1
            if other_case.distance_edible_ghost[i] == self.distance_edible_ghost[i]:
                dist_edible_ghosts += 1
            if other_case.distance_inedible_ghost[i] == self.distance_inedible_ghost[i]:
                dist_inedible_ghosts += 1
        
        # calculate our distance between cases and subtract from 1 to get the similarity value
        distc = (self.weight_pills * dist_pills) + (self.weight_power_pills * dist_powerpills) + (self.weight_edible_ghosts * dist_edible_ghosts) + (self.weight_ghosts * dist_inedible_ghosts)
        return 1 - distc

    def define_distances(self, board, x, y):
        grid = board.grid
        possible_actions = board.possible_actions(x, y)
        if "UP" not in possible_actions:
            __set_wall(0)
        if "RIGHT" not in possible_actions:
            __set_wall(1)
        if "DOWN" not in possible_actions:
            __set_wall(2)
        if "LEFT" not in possible_actions:
            __set_wall(3)
        
        index = 0
        for action in possible_actions:
            distances = board.breadth_first_search(action, x, y)

            if action == "UP":
                index = 0
            elif action == "RIGHT":
                index = 1
            elif action == "DOWN":
                index = 2
            elif action == "LEFT":
                index = 3
            
            # set the distance values for the index
            self.distance_pills[index] = distances[0]
            self.distance_powerpill[index] = distances[1]
            self.distance_inedible_ghost[index] = distances[2]
            self.distance_edible_ghost[index] = distances[3]

    def __set_wall(self, index):
        self.distance_pills[index] = "WALL"
        self.distance_powerpill[index] = "WALL"
        self.distance_inedible_ghost[index] = "WALL"
        self.distance_edible_ghost[index] = "WALL"