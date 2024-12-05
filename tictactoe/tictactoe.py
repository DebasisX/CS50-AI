"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

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
    x = 0
    y = 0
    for i in range(3): # Looping through all the values to count and finds whosoever's turn it is
        for j in range(3):
            if board[i][j] == X:
                x += 1
            elif board[i][j] == O:
                y += 1
            
    if x > y: # Whichever is greater, the opp. is the player 
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):  # Wherever there is some value just ignore and add the positions where there is Nothing.
        for j in range(3):
            if board[i][j] == O or board[i][j] == X:
                continue
            else:
                actions.add((i, j))
    return actions # Returns the set of all the moves 
    
def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    move = player(board)
    copy = deepcopy(board) 
    x = action[0]
    y = action[1] 
    valid = [0, 1, 2]
    if x in valid and y in valid:
        if board[x][y] == None:
            copy[x][y] = move
        else: 
            if board[x][y] != None:
                raise ValueError("Invalid move, cell is already occupied")
    else:
        raise ValueError("Invalid move")
    return copy
                                
def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking by comparing if the board state has reached one of ther winning states.
    win = [X, X, X]
    win2 = [O, O, O]
    for r in board:
        if win == r:
            return X
        elif win2 == r:
            return O 
    
    temp = deepcopy(board)
    # horizontally verifying
    for i in range(3):
        ls = []
        for r in range(3):
            ls.append(temp[r][i])
        if ls == win:
            return X 
        elif ls == win2:
            return O
    # diagonally verifying 
    new = []
    new.append(temp[0][0])
    new.append(temp[1][1])
    new.append(temp[2][2])
    new2 = []
    new2.append(temp[0][2])
    new2.append(temp[1][1])
    new2.append(temp[2][0])
    if new == win:   
        return X
    elif new == win2:
        return O
    elif new2 == win:
        return X     
    elif new2 == win2:
        return O
    return None 

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    # Checking if match has ended if there is no EMPTY places on board. 
    for r in board:
        for x in r:
            if x == EMPTY:
                return False

    return True
     
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # these are basic checks, returning the respective utility values.
    player = winner(board)
    if player == X:
        return 1
    elif player == O:
        return -1
    else:
        return 0    

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Recursively checking for the lowest or highest utility value, until a tie or a win is achieved.
    # Using the same function used in the Lecture.
    def max_val(board):
        move = ()
        if terminal(board):
            return utility(board), move
        else:
            v = -3
            for action in actions(board):
                res = result(board, action)
                minimum = min_val(res)[0]
                if minimum > v:
                    v = minimum
                    move = action
            return v, move # Returns the Max Utility value, along with the set of moves.

    def min_val(board):
        move = ()
        if terminal(board):
            return utility(board), move
        else:
            v = 3
            for action in actions(board):
                res = result(board, action)
                maximum = max_val(res)[0]
                if maximum < v:
                    v = maximum
                    move = action
            return v, move # Returns the Min Utility value, along with the set of moves.

    curr_player = player(board)

    if terminal(board):  # If terminal is None then Return.
        return None

    if curr_player == X:  # To win as X we need the moves which can lead to the MaxVal i.e 1. So we use MaxValue
        x = max_val(board)
        return x[1]

    else:
        x = min_val(board) # To win as X we need the moves which can lead to the MinVal i.e -1. So we use MinValue 
        return x[1]