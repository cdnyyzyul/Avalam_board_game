# monte carlo tree searcch
import numpy as np
import random
from avalam import *

class Node:
    def __init__(self, parent, ):
      self.incorrect = parent


# Monte Carlo tree node and ucb function

class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    return np.inf if n.N == 0 else n.U / n.N + C * np.sqrt(np.log(n.parent.N) / n.N)


# Monte Carlo Tree Search
def monte_carlo_tree_search(board, N=5000):
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n

    def expand(n):
        """expand the leaf node by adding all its children states"""
        if not n.children and not board.is_finished():
            n.children = {MCT_Node(state=board.clone().play_action(action), parent=n): action
                          for action in board.get_actions()}
        return select(n)

    def simulate(board):
        """simulate the utility of current state by random picking a step"""
        nb = board.clone()
        while not nb.is_finished():
            action = random.choice(list(nb.get_actions()))
            nb.play_action(action)
        v = nb.get_score()
        return v

    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        n.U += utility
        n.N += 1
        if n.parent:
            backprop(n.parent, utility)

    root = MCT_Node(state=board)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(child.state)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)

    action = root.children.get(max_state)

    return (action)



class MyAgent(Agent):

    """My Avalam agent."""

    def play(self, percepts, player, step, time_left):
        """
        This function is used to play a move according
        to the percepts, player and time left provided as input.
        It must return an action representing the move the player
        will perform.
        :param percepts: dictionary representing the current board
            in a form that can be fed to `dict_to_board()` in avalam.py.
        :param player: the player to control in this step (-1 or 1)
        :param step: the current step number, starting from 1
        :param time_left: a float giving the number of seconds left from the time
            credit. If the game is not time-limited, time_left is None.
        :return: an action
            eg; (1, 4, 1 , 3) to move tower on cell (1,4) to cell (1,3)
        """
     #   print("percept:", percepts)
        print("player:", player)
        print("step:", step)
        print("time left:", time_left if time_left else '+inf')

        # TODO: implement your agent and return an action for the current step.

        board = dict_to_board(percepts)
        actions = list(board.get_actions())
        print('actions', len(actions))

        return monte_carlo_tree_search(board)


if __name__ == "__main__":
    agent_main(MyAgent())
