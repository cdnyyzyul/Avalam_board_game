#!/usr/bin/env python3
"""
Avalam agent.
Copyright (C) 2022, <<<<<<<<<<< YOUR NAMES HERE >>>>>>>>>>>
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
from collections import Counter

infinity = math.inf

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda board, depth: depth > d


def game_heuristics(board, player):
    # towerdict = {}
    # for t in board.get_towers():
    #     towerdict[(t[0], t[1])] = t[2]
    # byheight = Counter(towerdict.values())
    # h2 = 0 if not byheight.get(-5) else byheight.get(-5)
    # h1 = 0 if not byheight.get(5) else byheight.get(5)
    # rt = board.get_score() + h1 + h2
    return board.get_score()


def h_alphabeta_search(board, player, cutoff=cutoff_depth(3), h=game_heuristics):

    def max_value(board, alpha, beta, depth):
        if board.is_finished():
            return board.get_score(), None
        if cutoff(board, depth):
            return h(board, player), None

        v, move = -infinity, None
        actions = board.get_actions()
        for a in actions:
            b = board.clone().play_action(a)
            v2, _ = min_value(b, alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                # print("max prune: ", v, move)
                return v, move
        # print("max: ", v, move)
        # print(board)
        return v, move

    def min_value(board, alpha, beta, depth):
        if board.is_finished():
            return board.get_score(), None
        if cutoff(board, depth):
            return h(board, player), None

        v, move = +infinity, None
        actions = board.get_actions()
        for a in actions:
            b = board.clone().play_action(a)
            v2, _ = max_value(b, alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                # print("min prune: ", v, move)
                return v, move
        # print("min: ", v, move)
        # print(board)
        return v, move

    if player == 1:
        _, action = max_value(board, -infinity, +infinity, 0)
    if player == -1:
        _, action = min_value(board, -infinity, +infinity, 0)

    return action


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

        return h_alphabeta_search(board, player)


if __name__ == "__main__":
    agent_main(MyAgent())

