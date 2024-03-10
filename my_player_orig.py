#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
-- Reference: git@github.com:BenJneB/Avalam.git  (Na Zhou)
Polytechnique Montréal

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

"""
from avalam import *
import math

infinity = math.inf

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda board, depth: depth > d


def game_heuristics(state):
   # strategy and rules
    return state[0].get_score()


def h_alphabeta_search(state, game, cutoff=cutoff_depth(2), h=game_heuristics):

    def max_value(state, alpha, beta, depth):
        if state[0].is_finished():
            return state[0].get_score(), None
        if cutoff(state, depth):
            return h(state), None

        v, move = -infinity, None
        for a, s in game.successors(state):
            v2, _ = min_value(s, alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                # print("max prune: ", v, move)
                return v, move
        # print("max: ", v, move)
        # print(state[0])
        return v, move

    def min_value(state, alpha, beta, depth):
        if state[0].is_finished():
            return state[0].get_score(), None
        if cutoff(state, depth):
            return h(state), None

        v, move = +infinity, None
        for a, s in game.successors(state):
            v2, _ = max_value(s, alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
#                print("min prune: ", v, move)
                return v, move
        # print("min: ", v, move)
        # print(state[0])
        return v, move

    if state[1] == 1:
        _, action = max_value(state, -infinity, +infinity, 0)
    if state[1] == -1:
        _, action = min_value(state, -infinity, +infinity, 0)

    return action


class MyAgent(Agent):

    """My Avalam agent."""

    # def __init__(self, name="MyAgent"):
    #     self.name = name

    # -- Reference: git @ github.com:BenJneB / Avalam.git  (Na Zhou)
    def successors(self, state):
        """The successors function must return (or yield) a list of
        pairs (a, s) in which a is the action played to reach the
        state s; s is the new state, i.e. a triplet (b, p, st) where
        b is the new board after the action a has been played,
        p is the player to play the next move and st is the next
        step number.
        """
        board = state[0]
        player = state[1]
        stepnumber = state[2]
        for action in board.get_actions():
            yield (action, (board.clone().play_action(action), (-1) * player, stepnumber + 1))


    # def evaluate(self, state):
    #     """The evaluate function must return an integer value
    #     representing the utility function of the board.
    #     """
    #     board = state[0]
    #     tower = 0
    #     towMax = 0
    #     towIsol = 0
    #     for i in range(board.rows):
    #         for j in range(board.columns):
    #             """number of tower for each player"""
    #             if board.m[i][j] < 0:
    #                 tower -= 1
    #             elif board.m[i][j] > 0:
    #                 tower += 1
    #
    #             """number of tower (height:5) for each player"""
    #             if board.m[i][j] == -5:
    #                 towMax -= 1
    #             elif board.m[i][j] == 5:
    #                 towMax += 1
    #             number = abs(board.m[i][j])
    #             countNeigh = 0
    #             countPoss = 0
    #             if (not board.is_tower_movable(i, j) and not (abs(board.m[i][j]) == 5)):
    #                 if board.m[i][j] < 0:
    #                     towIsol -= 1
    #                 elif board.m[i][j] > 0:
    #                     towIsol += 1
    #
    #     return tower + 5 * towMax + 5 * towIsol


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
        state = (board, player, step)
        return h_alphabeta_search(state, self)


if __name__ == "__main__":
    agent_main(MyAgent())

