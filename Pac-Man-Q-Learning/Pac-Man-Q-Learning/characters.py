class Character:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def move(self, action):
        if action == "UP":
            self.y -= 1
        elif action == "DOWN":
            self.y += 1
        elif action == "RIGHT":
            self.x += 1
        elif action == "LEFT":
            self.x -= 1

class Pacman(Character):
    def __init__(self):
        self.pills_eaten = 0
        self.score = 0
        # Define the starting point for all Pac-Man agents in the grid
        self.x = 0
        self.y = 8

class Ghost(Character):
    def __init__(self, aggression):
        self.aggression = aggression
        self.x = 4
        self.y = 7


