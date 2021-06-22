"""
Tic Tac Toe Player
"""

import numpy as np
from copy import deepcopy
from random import randrange

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    initial = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]

    # convert into NumPy array
    return np.asarray(initial)


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if np.all(board == EMPTY):
        return X
    elif np.all(board != EMPTY):
        return None
    elif np.count_nonzero(board == X) > np.count_nonzero(board == O):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions_set.add((i, j))

    return actions_set if len(actions_set) else None


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = deepcopy(board)
    marker = player(board_copy)
    i, j = action

    try:
        if board_copy[i][j] != EMPTY:
            raise ValueError("Cell is already taken!")
        board_copy[i][j] = marker
        return board_copy
    except ValueError as ve:
        print(ve)
        return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    def check_rows(board):
        for row in board:
            if len(set(row)) == 1:
                return row[0]
        return None

    def check_diagonals(board):
        length = len(board)

        if len(set([board[i][i] for i in range(length)])) == 1:
            return board[0][0]
        if len(set([board[i][length-i-1] for i in range(length)])) == 1:
            return board[0][length-1]
        return None

    def check_win(board):
        # check rows, then transpose matrix to check columns
        for new_board in [board, np.transpose(board)]:
            result = check_rows(new_board)
            if result:
                return result
        return check_diagonals(board)

    return check_win(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return bool(winner(board) or not player(board))


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_check = winner(board)
    if winner_check == X:
        return 1
    elif winner_check == O:
        return -1
    else:
        return 0


def max_value(board, alpha=float("-inf"), beta=float("inf")):
    value = float("-inf")

    if terminal(board):
        return utility(board), None

    for action in actions(board):
        temp_max, _ = min_value(result(board, action), alpha, beta)
        if temp_max > value:
            value = temp_max
            best_move = action
        alpha = max(alpha, value)
        if beta <= alpha:
            break
    return value, best_move


def min_value(board, alpha=float("-inf"), beta=float("inf")):
    value = float("inf")

    if terminal(board):
        return utility(board), None

    for action in actions(board):
        temp_min, _ = max_value(result(board, action), alpha, beta)
        if temp_min < value:
            value = temp_min
            best_move = action
        beta = min(beta, value)
        if beta <= alpha:
            break
    return value, best_move


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if np.all(board == EMPTY):
        return (randrange(3), randrange(3))

    _, best_move = max_value(board) if player(board) == X else min_value(board)
    return best_move
