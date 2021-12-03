"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty_field_counter = 0
    return sum([1 for field in row for row in board if field == EMPTY])
    for row in board:
        for field in row:
            if field == EMPTY:
                empty_field_counter += 1
    return X if empty_field_counter % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for row_counter in range(len(board)):
        for column_counter in range(len(board[row_counter])):
            if board[row_counter, column_counter] == EMPTY:
                possible_actions.append((row_counter, column_counter))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    update_board = copy.deepcopy(board)
    if board[action(0)][action[1]] == EMPTY:
        update_board[action(0)][action(1)] = player(board)
    else:
        raise ValueError("Field already in use")
    return update_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
