from random import randint
from random import uniform
from characters import *
from board import Board
from case import Case

class Episode:
    """
    This class is used to represent a single episode for an agent using an input q-table and case base.
    Simulation of an episode terminates once all the pills have been eaten or Pac-Man dies to a ghost
    """

    def __init__(self):
        # initialize our agent for the episode and the board with one non-aggressive ghost
        self.agent = Pacman()
        self.board = Board()
        self.board.add_ghost(Ghost(0, 12, 11))
        self.board.add_ghost(Ghost(0, 13, 11))
        self.board.add_ghost(Ghost(0, 14, 11))
        self.board.add_ghost(Ghost(0, 15, 11))
        self.alpha = .1
        self.gamma = .98

    # simulates an entire episode, which equates to one Pac-Man level in this case
    def simulate(self, case_base):
        board = self.board
        agent = self.agent
        previous_case = Case()
        
        previous_case.define_distances(board, agent.x, agent.y)
        current_case = previous_case
        cycles = 0
        dead = False
        # episode terminates when all pills have been eaten (power pills included), Pac-Man dies, or agent takes too long
        while agent.pills_eaten < 264 and not dead and cycles < 500:

            # calculate the similarity of every case to the current case and select our most similar
            similarities = []
            for past_case in case_base:
                similarities.append(past_case.similarity(current_case))
                
            similarity = max(similarities)
            similar_case = case_base[similarities.index(max(similarities))]

            # determine our possible actions and best action based on the q-table
            possible_actions = board.possible_actions(agent.x, agent.y)
            action = max(similar_case.quality, key = similar_case.quality.get)

            # if action not possible, take a random action
            if action not in possible_actions:
                action = possible_actions[randint(0, len(possible_actions) - 1)]

            # move our agent until they reach the next intersection and get cumulative reward
            agent.move(action)
            reward = board.get_reward(agent)
            if not board.is_intersection(agent.x, agent.y):
                agent.move(action)
                reward += board.get_reward(agent)
                
                
            # define a new case based on the current situation
            next_case = Case()
            next_case.define_distances(board, agent.x, agent.y)

            # update our quality values for previous case
            next_case_quality_values = next_case.quality.values()
            previous_case.quality[action] += self.alpha * similarity * reward + self.gamma * max(next_case_quality_values) - previous_case.quality[action]
            if previous_case.similarity(current_case) < .99:
                case_base.append(current_case)

            previous_case = current_case

            # move our ghosts and check if Pac-Man moved into a ghost
            for ghost in board.ghosts:
                possible_ghost_actions = board.possible_actions(ghost.x, ghost.y)
                random_action = randint(0, len(possible_ghost_actions) - 1)
                ghost.move(possible_ghost_actions[random_action])
                
                if agent.x == ghost.x and agent.y == ghost.y:
                    dead = True
                    break
            cycles += 1
            
        print("Episode completed. Agent score: " + str(agent.score))
        file = open("results.txt", "a")
        file.write(str(agent.score))
        file.close()
                