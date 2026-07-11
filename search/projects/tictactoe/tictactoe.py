"""
Tic Tac Toe Player
"""

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
    x_count = sum(row.count("X") for row in board)
    o_count = sum(row.count("O") for row in board)
    return "O" if x_count > o_count else "X"

  


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    all_actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == EMPTY):
                all_actions.add((i,j))
    return all_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    
    new_board[action[0]][action[1]] = player(board)
    return new_board
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Checking for first row
    if(board[0][0] == board[0][1] == board[0][2] and board[0][0] != EMPTY):
        return board[0][0]
    
    # Checking for second row
    if(board[1][0] == board[1][1] == board[1][2] and board[1][0] != EMPTY):
        return board[1][0]
    
    # Checking for third row
    if(board[2][0] == board[2][1] == board[2][2] and board[2][0] != EMPTY ):
        return board[2][0]
    

    # Checking for first column
    if(board[0][0] == board[1][0] == board[2][0] and board[0][0] != EMPTY):
        return board[0][0]
    
    # Checking for second column
    if(board[0][1] == board[1][1] == board[2][1] and board[0][1] != EMPTY):
        return board[0][1]
    
    # Checking for third column
    if(board[0][2] == board[1][2] == board[2][2] and board[0][2] != EMPTY):
        return board[0][2]

    # left to right diagnol check
    if(board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY):
        return board[0][0]
    

    # right to left diagnol check
    if(board[0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY):
        return board[0][2]
    

    
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board)):
        return True
    return not any(EMPTY in row for row in board)
  
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if( winner(board) == "X"):
        return 1
    if(winner(board) == "O"):
        return -1
    return 0
    


def minimax(board):
    """
    Returns the optimal action for the current_player player on the board.
    """ 
    if(terminal(board)):
        return None
    
    optimal_action = None
 

    if(player(board) == "O"):

        best_score = float("inf")
        for move in actions(board):
            sc = mini(result(board,move))
            if(sc<best_score):
                best_score = sc
                optimal_action = move
    else:
        best_score = float("-inf")
        for move in actions(board):
            sc = maxi(result(board,move))
            if(sc>best_score):
                best_score = sc
                optimal_action = move


    return optimal_action

# board , (0,1)
def mini(board):

    if(terminal(board)):
        return utility(board)

    
    best_score = float('inf')
    for mv in actions(board):
        best_score = min(best_score,maxi(result(board,mv)))
    return best_score


def maxi(board):
    if(terminal(board)):
        return utility(board)
    best_score = float("-inf")
    for mv in actions(board):
        best_score = max(best_score,mini(result(board,mv)))

    return best_score
