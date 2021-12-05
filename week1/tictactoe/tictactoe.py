"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np
from time import sleep

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
    not_empty_field_counter = 0
    for row in board:
        for field in row:
            if field != EMPTY:
                not_empty_field_counter += 1
    return X if not_empty_field_counter % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = []
    for row_counter in range(len(board)):
        for column_counter in range(len(board[row_counter])):
            if board[row_counter][column_counter] == EMPTY:
                possible_actions.append((row_counter, column_counter))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    update_board = copy.deepcopy(board)
    if board[action[0]][action[1]] == EMPTY:
        update_board[action[0]][action[1]] = player(board)
    else:
        raise ValueError("Field already in use")
    #print(player(board))
    #for row in board:
    #    print(row)
    #print()
    #sleep(2)
    return update_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # if we could know the last move made, we could lessen the amount of possible options we have to check for bigger than 3x3 boards
    winner = check_for_horizontal_win(board)
    
    #find out who made the last move, only that one can win
    current_player = X if player(board) == O else O
    
    if winner == current_player:
        return current_player
    
    #check first diagonal
    if board[0][0] == current_player:
        if board[1][1] == current_player:
            if board[2][2] == current_player:
                return current_player


    #rotate board 90 degrees
    board_copy = np.rot90(board, k=1)
    winner = check_for_horizontal_win(board) 
    if winner == current_player:
        return current_player
    
    #check second diagonal
    if board[0][0] == current_player:
        if board[1][1] == current_player:
            if board[2][2] == current_player:
                return current_player


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) == X or winner(board) == O:
        return True
    for row in board:
        for field in row:
            if field == EMPTY:
                return False
    return True


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    move_values = []
    current_player = player(board)
    actions_list = actions(board)
    for action in actions_list:
        move_value =max_value(result(board,action)) if current_player == X else min_value(result(board,action))
        print(f"for action: {action}, best value: {move_value}")
        move_values.append(move_value)
    optimal_move_index = move_values.index(max(move_values)) if current_player == X else move_values.index(min(move_values))
    print(f"best action: {actions_list[optimal_move_index]}, value: {max(move_values) if current_player == X else min(move_values)}")
    return actions_list[optimal_move_index]


def max_value(board):
    #for row in board:
    #    print(row)
    #print()
    #sleep(2)
    if terminal(board):
        return utility(board)
    value = float('-inf')
    for action_index,action in enumerate(actions(board)):
        value = max(value, min_value(result(board, action)))
    return value


def min_value(board):
    #for row in board:
    #    print(row)
    #print()
    #sleep(2)
    if terminal(board):
        return utility(board)
    value = float('inf')
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value


def check_for_horizontal_win(board):
    current_player = X if player(board) == O else O
    for row in board:
        consecutive_counter = 0
        for field in row:
            if field != current_player:
                consecutive_counter = 0
                break
            else:
                consecutive_counter += 1
                if consecutive_counter > 2:
                    return current_player
    return None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0