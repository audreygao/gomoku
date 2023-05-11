from __future__ import absolute_import, division, print_function
from math import sqrt, log
from game import Game, WHITE, BLACK, EMPTY
import copy
import time
import random

class Node:
    def __init__(self, state, actions, parent=None):
        self.state = (state[0], copy.deepcopy(state[1]))
        self.num_wins = 0 #number of wins at the node
        self.num_visits = 0 #number of visits of the node
        self.parent = parent #parent node of the current node
        self.children = [] #store actions and children nodes in the tree as (action, node) tuples
        self.untried_actions = copy.deepcopy(actions) #store actions that have not been tried
        simulator = Game(*state)
        self.is_terminal = simulator.game_over

BUDGET = 1000

class AI:
    def __init__(self, state):
        self.simulator = Game()
        self.simulator.reset(*state) #using * to unpack the state tuple
        self.root = Node(state, self.simulator.get_actions())

    def mcts_search(self):

        iters = 0
        action_win_rates = {} #store the table of actions and their ucb values

        # Monte Carlo Tree Search Loop
        while(iters < BUDGET):
            if ((iters + 1) % 100 == 0):
                print("\riters/budget: {}/{}".format(iters + 1, BUDGET), end="")

            # select a node, rollout, and backpropagate
            node = self.select(self.root)
            reward = self.rollout(node)
            winner = BLACK if reward[BLACK] == 1 else WHITE
            self.backpropagate(node, winner)
            iters += 1
        print()

        # Return the best action, and the table of actions and their win values 
        _, action, action_win_rates = self.best_child(self.root, 0)

        return action, action_win_rates

    def select(self, node):

        while (not node.is_terminal):
            if len(node.untried_actions) > 0:
                return self.expand(node)
            else:
                node, _, _ = self.best_child(node, 1)
        return node

    def expand(self, node):

        child_node = None #choose a child node to grow the search tree
        action = node.untried_actions.pop(0)
        
        self.simulator.reset(*node.state)
        self.simulator.place(*action)
        child_node = Node(self.simulator.state(), self.simulator.get_actions(), node)
        node.children.append((action, child_node))

        return child_node

    def best_child(self, node, c=1): 

        # determine the best child and action by applying the UCB formula

        best_child_node = None # to store the child node with best UCB
        best_action = None # to store the action that leads to the best child
        action_ucb_table = {} # to store the UCB values of each child node (for testing)

        max_ucb = 0
        for child in node.children:
            action, child_node = child
            action_ucb_table[action] = child_node.num_wins / child_node.num_visits + c * sqrt(2*log(node.num_visits)/child_node.num_visits)
            if action_ucb_table[action] > max_ucb:
                max_ucb = action_ucb_table[action]
                best_action, best_child_node = action, child_node

        # best_action, best_child_node = max(action_ucb_table, key=action_ucb_table.get)
        return best_child_node, best_action, action_ucb_table

    def backpropagate(self, node, result):

        while (node is not None):
            # backpropagate 
            node.num_visits += 1
            
            player, _ = node.state
            if player != result:
                node.num_wins += 1
                
            node = node.parent

    def rollout(self, node):

        # rollout
        self.simulator.reset(*node.state)
        while not self.simulator.game_over:
            rand_action = self.simulator.rand_move()
            self.simulator.place(*rand_action)

        # Determine reward indicator from result of rollout
        reward = {}
        if self.simulator.winner == BLACK:
            reward[BLACK] = 1
            reward[WHITE] = 0
        elif self.simulator.winner == WHITE:
            reward[BLACK] = 0
            reward[WHITE] = 1
        return reward
