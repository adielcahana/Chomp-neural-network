#board is a list of rows of the same size.
#each entry of board is 0 (invalid move) or 1 (valid move).
#the function should return a valid move, for example [0,0] (which is a loosing move, of course)
def move(board):
    import random

    win=winning_move(board)
    if win!=False:
        return win

    moves = []
    real_width=len(board[0])
    for i in range (0,len(board)):
        for j in range (0,real_width):
            if i==0 and j==0:
                continue
            if board[i][j]==1:
                moves.append([i,j])
            else:
                real_width=j
                break
    if len(moves)==0:
        return [0,0]
    return random.choice(moves)

def winning_move(board):
    if board[0][1]==0 and board[1][0]==1:
        return [1,0]
    if board[1][0]==0 and board[0][1]==1:
        return [0,1]

    return False