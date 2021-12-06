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
    try:
        if board[action[0]][action[1]] == EMPTY:
            update_board[action[0]][action[1]] = player(board)
        else:
            print("Field already in use")
            raise ValueError("Field already in use")
    except IndexError as ie:
        print(ie)
        raise IndexError
    return update_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # if we could know the last move made, we could lessen the amount of possible options we have to check for bigger than 3x3 boards
    winner_players = [X, O]

    possible_winner = check_for_horizontal_win(board)
    if possible_winner in winner_players:
        return possible_winner

    #check first diagonal
    for winner_player in winner_players:
        is_won = True
        for i in range(len(board[0])):
            if board[i][i] != winner_player:
                is_won = False
                break
        if is_won:
            return winner_player

    #rotate board 90 degrees
    board_copy = np.rot90(board, k=1)

    possible_winner = check_for_horizontal_win(board_copy) 
    if possible_winner in winner_players:
        return possible_winner
    
    #check second diagonal
    for winner_player in winner_players:
        is_won = True
        for i in range(len(board[0])):
            if board_copy[i][i] != winner_player:
                is_won = False
                break
        if is_won:
            return winner_player
    return None

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
    move_values = []
    current_player = player(board)
    actions_list = actions(board)
    for action in actions_list:
        move_value =max_value(result(board,action)) if current_player == O else min_value(result(board,action))
        print(f"for action: {action}, best value: {move_value}")
        move_values.append(move_value)
        if current_player == O and move_value == -1: 
            break
        if current_player == X and move_value == 1:
            break
    optimal_move_index = move_values.index(max(move_values)) if current_player == X else move_values.index(min(move_values))
    print(f"best action: {actions_list[optimal_move_index]}, value: {max(move_values) if current_player == X else min(move_values)}")
    return actions_list[optimal_move_index]


def max_value(board,local_min=float('-inf'), local_max=float('inf')):
    value = float('-inf')
    if terminal(board):
        value = utility(board)
        return value
    for action in actions(board):
        new_possible_value = min_value(result(board,action),local_min=local_min, local_max=local_max)
        if local_max <= new_possible_value:
            return new_possible_value
        value = max(value, new_possible_value)
        local_min = value
    return value


def min_value(board,local_min=float('-inf'), local_max=float('inf')):
    value = float('inf')
    if terminal(board):
        value = utility(board)
        return value
    for action in actions(board):
        new_possible_value = max_value(result(board, action),local_min=local_min, local_max=local_max)
        if local_min >= new_possible_value:
            return new_possible_value
        value = min(value, new_possible_value)
        local_max = value
    return value


def check_for_horizontal_win(board):
    players = [X, O]
    for player in players:
        for row in board:
            consecutive_counter = 0
            for field in row:
                if field != player:
                    consecutive_counter = 0
                    break
                else:
                    consecutive_counter += 1
                    if consecutive_counter > len(board)-1:
                        return player
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