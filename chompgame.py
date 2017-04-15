def initial_board(width,height):
    board = [None]*height
    board[0] = [1] + [1] * (width - 1)
    for i in range(1, height):
        board[i] = [1] * width
    return board

def make_move(board,move,width,height):
    if move[1]>=width or move[1]<0:
        print ('out of range' + str(move))
        return False
    if move[0]>=height or move[0]<0:
        print ('out of range' + str(move))
        return False
    if board[move[0]][move[1]]==0:
        print ('bad move' + str(move))
        return False

    for i in range(move[0],height):
        for j in range(move[1],width):
            board[i][j]=0

    # print_board(board)
    if move[0]==0 and move[1]==0:
        return False
    return True

def print_board(board):
    print("   ", end="")
    for i in range(len(board)):
        print(i, end="  ")
    print()
    for i in range(0,len(board)):
            print(len(board) -1 - i, end=" ")
            print(board[len(board)-i-1])
    print ("")

def copy_board(board,width,height):
    copyboard=[None]*height
    for i in range(0,height):
        copyboard[i]=list(board[i])
    return copyboard


import time

def play(player1,player2,width,height):

    board = initial_board(width,height)
    player1time=0
    player2time=0

    # print_board(board)

    while True:
        print_board(board)

        start= time.clock()
        move = player1.move(copy_board(board,width,height))
        end= time.clock()
        player1time+=end-start
        if player1time>10:
            print("player 1 out of time")
        if player1time>10 or not make_move(board,move,width,height):
            return 2 #player 2 has won

        print_board(board)

        start= time.clock()
        str = input("Enter move input: ") # player2.move(copy_board(board,width,height))
        move = [int(str.split(",")[0]),int(str.split(",")[1])]
        end= time.clock()
        player2time+=end-start
        if player2time>1000:
            print("player 2 out of time")
        if player2time>1000 or not make_move(board,move,width,height):
            return 1 #player 1 has won



#player1.py and player2.py must contain an implemenation of the function move(board)
#which returns a valid move [i,j]
def main():

    width = 9  # of board
    height = 9  # of board
    import player3
    import player2
    games = 2

    player1wins = 0
    start = time.clock()
    for i in range(0,games):
        if play(player3,player2,width,height)==1:
            player1wins+=1
    end= time.clock()
    runtime= end-start

    return 'Player 3 won ' + str(player1wins) + ' out of ' + str(games) + ' games of size '+str(height) + 'x'+str(width)+ '. Total Game Time: '+str(runtime)+' sec'

print (main())

