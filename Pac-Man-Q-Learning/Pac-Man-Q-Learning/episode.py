from random import randint
from characters import *
from board import Board
from case import Case

class Episode:
    """
    This class is used to represent a single episode for an agent using an input q-table and case base.
    Simulation of an episode terminates once all the pills have been eaten or Pac-Man dies to a ghost
    """
    alpha = .1
    gamma = .98

    def __init__(self):
        # initialize our agent for the episode and the board with one non-aggressive ghost
        self.agent = Pacman()
        self.board = Board()
        self.board.add_ghost(Ghost(0))

    def simulate(self, qtable, case_base):
        action = "NONE"
        board = self.board
        agent = self.agent
        case = case_base[0]
        # episode terminates when all pills have been eaten (power pills included) or Pac-Man dies
        while agent.pills_eaten < 98 and not dead:
            dead = False
            if board.is_intersection(agent.x, agent.y):
                # calculate the similarity of every case to the current case and select our most similar
                similarities = []
                for past_case in case_base:
                    similarities.append(past_case.similarity(case))
                
                similarity = max(similarities)
                similar_case = case_base[similarities.index(max(similarities))]

                # determine our possible actions and best action based on the q-table
                possible_actions = board.possible_actions(agent.x, agent.y)
                best_action_index = qtable[case_base.index(similar_case)].index(max(qtable[case_base.index(similar_case)]))
                if best_action_index == 0:
                    action == "UP"
                elif best_action_index == 1:
                    action == "RIGHT"
                elif best_action_index == 2:
                    action == "DOWN"
                elif best_action_index == 3:
                    action == "LEFT"
                
                # if action not possible, take next best possible action
                if action not in possible_actions:
                   action = possible_actions[0]

                agent.move(action)
                reward = board.get_reward(agent)
                
                # define a new case based on the current situation
                new_case = Case()
                new_case.define_distances(board, x, y)

                # update our q table 
                qtable[case_base.index(case)][best_action_index] += self.alpha * (similarity * reward + self.gamma * max(qtable[new_case]) - qtable[case_base.index(case)][best_action_index])

                if similar_case.similarity(new_case) < .99:
                    case_base.append(new_case)
                    qtable.append([0] * 4)
            else:
                agent.move(action)
                reward += board.get_reward(agent)
            
            # move our ghosts check if Pac-Man moved into a ghost
            for ghost in board.ghosts:
                possible_ghost_actions = board.possible_actions(ghost.x, ghost.y)
                random_action = randint(0, len(possible_ghost_actions) - 1)
                ghost.move(possible_ghost_actions[random_action])
                
                if agent.x == ghost.x and agent.y == ghost.y:
                    dead = true
                    break
            
        print("Episode completed. Agent score: " + str(agent.score))
        file = open("results.txt", "a")
        file.write(agent.score)
        file.close()
                