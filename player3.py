import random
import pickle
with open('false.pickle', 'rb') as fp:
    falseboard = pickle.load(fp)

def make_move1(board,move,width,height):
    for i in range(move[0],height):
        for j in range(move[1],width):
            board[i][j]=0

def translate(board):
    moves = []
    real_width=len(board[0])
    for i in range (0,len(board)):
        for j in range (0,real_width):
            if board[i][j]==1:
                moves.append((i,j))
            else:
                real_width=j
                break
    return frozenset(moves)

def copy_board1(board, width, height):
    copyboard=[None]*height
    for i in range(0,height):
        copyboard[i]=list(board[i])
    return copyboard

def move(board):
    moves = []
    real_width=len(board[0])
    for i in range (0,len(board)):
        for j in range (0,real_width):
            if board[i][j]==1:
                moves.append([i,j])
            else:
                real_width=j
                break
    if len(moves)==0:
        return [0,0]

    try:
        if (len(board[0]) < 8 and len(board) < 8) or (board[0][7] == 0 and board[7][0] == 0):
            for move in moves:
                try_board = copy_board1(board, len(board[0]), len(board))
                make_move1(try_board, move, len(board[0]), len(board))
                if translate(try_board) in falseboard:
                    return move
    except IndexError:
        pass

    return random.choice(moves)


