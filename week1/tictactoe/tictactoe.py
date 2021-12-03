"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

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
    
    # if we could know the last move made, we could lessen the amount of possible options we have to check for bigger than 3x3 boards
    winner = check_for_horizontal_win(board)
    
    #find out who made the last move, only that one can win
    player = X if player(board) == O else O
    if winner != None:
        return winner
    
    #check first diagonal
    for i in range(3):
        if board[i][i] != player:
            break
        return player
    
    #rotate board 90 degrees
    board_copy = np.rot90(board, k=1)
    winner = check_for_horizontal_win(board) 
    if winner != None:
        return winner
    
    #check second diagonal
    for i in range(3):
        if board[i][i] != player:
            break
        return player
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for row in board:
        for field in row:
            if board[row][field] == EMPTY:
                return False
    return True


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

def check_horizontal_for_win(board):
    winner = X
    for row in board:
        consecutive_counter = 0
        for field in row:
            if field == winner:
                consecutive_counter += 1
                if consecutive_counter > 2:
                    return winner
            else:
                consecutive_counter = 1
                winner = field