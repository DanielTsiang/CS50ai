"""
Tic Tac Toe Player
"""

from copy import deepcopy
from random import randrange

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
    count = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                count += 1

    if board == initial_state():
        return X
    if count % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid action!")

    board_copy = deepcopy(board)
    board_copy[action[0]][action[1]] = player(board)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
            else:
                return None

    # check rows
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] == X:
                return X
            elif board[0][j] == O:
                return O
            else:
                return None

    # check top-left to bottom-right diagonal
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
        else:
            return None

    # check bottom-left to top-right diagonal
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
        else:
            return None

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner_check = winner(board)
    if winner_check in [X, O]:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_check = winner(board)
    if (winner_check == X):
        return 1
    elif (winner_check == O):
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if board == initial_state():
        return (randrange(3), randrange(3))
    
    alpha = float("-inf")
    beta = float("inf")

    if player(board) == X:
        return max_value(board, alpha, beta)[1]
    else:
        return min_value(board, alpha, beta)[1]


def max_value(board, alpha, beta):
    if terminal(board):
        return [utility(board), None]

    value = float("-inf")
    for action in actions(board):
        temp_max = min_value(result(board, action), alpha, beta)[0]
        if temp_max > value:
            value = temp_max
            best_move = action
        alpha = max(alpha, temp_max)
        if alpha >= beta:
            break
    return [value, best_move]


def min_value(board, alpha, beta):
    if terminal(board):
        return [utility(board), None]

    value = float("inf")
    for action in actions(board):
        temp_min = max_value(result(board, action), alpha, beta)[0]
        if temp_min < value:
            value = temp_min
            best_move = action
        beta = min(beta, temp_min)
        if alpha >= beta:
            break
    return [value, best_move]
