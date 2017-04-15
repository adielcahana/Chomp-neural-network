import winboard
import math
import random
import pickle
import time
import GenAlg as GA
import neuralNet as NN
import player1
import player2

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
    for i in range(0,len(board)):
            print(board[len(board)-i-1])
    print ("")

def copy_board(board,width,height):
    copyboard=[None]*height
    for i in range(0,height):
        copyboard[i]=list(board[i])
    return copyboard

def validMove(move, board ,width, height):
    if move[1] >= width or move[1] < 0:
        return False
    if move[0] >= height or move[0] < 0:
        return False
    if board[move[0]][move[1]] == 0:
        return False
    if move[0] == 0 and move[1] == 0:
        return False
    return True

def train1(numOfTraining):
    width = 8   # of board
    height = 8  # of board

    with open('true.pickle', 'rb') as fp:
        trueboard = list(pickle.load(fp))
    with open('false.pickle', 'rb') as fp:
        falseboard = list(pickle.load(fp))

    numInput, numOutput, numHiddenLayer, neuronPerLayer = 8, 1, 1, 8
    net = NN.NeuralNet(numInput, numOutput, numHiddenLayer, neuronPerLayer)
    ga = GA.GenAlg()
    # with open('ga-data_step.pickle', 'rb') as fp:
    #     print(fp.name)
    #     ga = pickle.load(fp)


    for j in range(numOfTraining):
        start = time.clock()
        print("iteration #: " + str(j))
        board = initial_board(width, height)

        winboard.detranslate(random.choice(falseboard), board)
        for genome in ga:
            net.putWeights(genome.weights)
            move1 = net.move(board, True)
            genome.fitness = ga.Fitness(0.0, move1[0])

        for genome in ga:
            print(genome.fitness, end=" ")
        print()
        ga.Epoch()

        winboard.detranslate(random.choice(trueboard), board)
        for genome in ga:
            net.putWeights(genome.weights)
            move1 = net.move(board, True)
            genome.fitness = ga.Fitness(1.0, move1[0])

        for genome in ga:
            print(genome.fitness, end=" ")
        print()
        ga.Epoch()

        end = time.clock()
        runtime = end - start
        print("runtime is " + str(runtime))

    pickle.dump(ga, open('ga_tftrain_sig.pickle', 'wb'))

def train2(numOfTraining):
    width = 8   # of board
    height = 8  # of board

    with open('true.pickle', 'rb') as fp:
        trueboard = list(pickle.load(fp))
    with open('false.pickle', 'rb') as fp:
        falseboard = list(pickle.load(fp))

    numInput, numOutput, numHiddenLayer, neuronPerLayer = 8, 1, 1, 2
    net = NN.NeuralNet(numInput, numOutput, numHiddenLayer, neuronPerLayer)
    ga = GA.GenAlg()
    # elite = set()

    # with open('elite.pickle', 'rb') as fp:
    #     print(fp.name)
    #     print(sorted(pickle.load(fp).population, key=GA.Genome.getFitness)[-1:-101])
    #     ga.population = sorted(pickle.load(fp).population, key = GA.Genome.getFitness)[-1:-101]
    # random.shuffle(ga.population)
    # for genome in ga.population:
    #     genome.fitness = 0.0

    for j in range(numOfTraining):
        start = time.clock()
        print("iteration #: " + str(j))
        trueboards = random.sample(trueboard, 100)
        falseboards = random.sample(falseboard, 100)

        for i in range(100):
            tb = initial_board(width, height)
            fb = initial_board(width, height)
            winboard.detranslate(trueboards[i], tb)
            winboard.detranslate(falseboards[i], fb)
            for genome in ga:
                net.putWeights(genome.weights)
                move1 = net.move(tb, False)
                move2 = net.move(fb, False)
                if move1[0] == 1.0:
                    genome.fitness += 1
                if move2[0] == 0.0:
                    genome.fitness += 1

        ga.population.sort(key=GA.Genome.getFitness)
        ga.population.reverse()
        for genome in ga:
            print(genome.fitness, end = " ")
            if genome.fitness == 200:
                print("solution is genome " + str(ga.population.index(genome)))
                pickle.dump(ga, open('ga_data_tftrain_step.pickle', 'wb'))
                # ga.population = list(elite)
                # pickle.dump(ga, open('elite.pickle', 'wb'))
                exit()
            # elif genome.fitness > 100:
                # elite.add(genome.copy())
        # print()
        # print(len(elite))

        if j == numOfTraining - 1:
            pickle.dump(ga, open('ga_data_tftrain_step.pickle', 'wb'))
            # print(len(elite))
            # ga.population = list(elite)
            # pickle.dump(ga, open('elite.pickle', 'wb'))
            exit()

        ga.Epoch()

        end = time.clock()
        runtime = end - start
        print("runtime is " + str(runtime))

def train3(numOfTraining):
    width = 8   # of board
    height = 8  # of board

    with open('true.pickle', 'rb') as fp:
        trueboard = list(pickle.load(fp))
    with open('false.pickle', 'rb') as fp:
        falseboard = list(pickle.load(fp))
    # with open('net.pickle', 'rb') as fp:
    #     net = pickle.load(fp)

    numInput, numOutput, numHiddenLayer, neuronPerLayer = 8, 1, 1, 48
    net = NN.NeuralNet(numInput, numOutput, numHiddenLayer, neuronPerLayer)

    for j in range(numOfTraining):
        # start = time.clock()
        print("iteration #: " + str(j))
        trueboards = random.sample(trueboard, 400)
        falseboards = random.sample(falseboard, 100)

        for i in range(400):
            tb = initial_board(width, height)
            winboard.detranslate(trueboards[i], tb)
            net.train(tb, [1.0])
            if (i % 4):
                fb = initial_board(width, height)
                winboard.detranslate(falseboards[i%100], fb)
                net.train(fb, [0.0])



        # end = time.clock()
        # runtime = end - start
        # print("runtime is " + str(runtime))

    # trueboards = random.sample(trueboard, 100)
    # falseboards = random.sample(falseboard, 100)
    avg_true = 0
    avg_false = 0
    avg_ans_false = 0
    avg_ans_true = 0

    trueboards = random.sample(trueboard, 100)
    falseboards = random.sample(falseboard, 100)
    for i in range(100):
        tb = initial_board(width, height)
        fb = initial_board(width, height)
        winboard.detranslate(trueboards[i], tb)
        winboard.detranslate(falseboards[i], fb)
        move1 = net.move(tb, True)
        move2 = net.move(fb, True)
        avg_ans_true += move1[0]
        avg_ans_false += move2[0]
        if math.fabs(move1[0] - 1.0) <= 0.1:
            avg_true += 1
        if  math.fabs(move2[0] - 0.0) <= 0.1:
            avg_false += 1

    print("avg_true: " + str(avg_true/100) + " avg_false: " + str(avg_false / 100) )
    print("avg_true_ans: " + str(avg_ans_true / 100) + " avg_false_ans: " + str(avg_ans_false / 100))
    pickle.dump(net, open('net.pickle', 'wb'))

def trainTable(numOfIter, player, width, height):
    board = initial_board(width, height)
    true = set()
    false = set()
    i = 0

    while(i < numOfIter):
        trns_board = winboard.translate(board)
        isWin = winboard.wins(trns_board)
        if isWin == False:
            false.add(trns_board)
        else:
            true.add(trns_board)

        move = player.move(board)
        if not make_move(board, move, width, height):
            board = initial_board(width,height)
            i += 1

    print(len(true))
    print(len(false))
    pickle.dump(true, open('true.pickle', 'wb'))
    pickle.dump(false, open('false.pickle', 'wb'))

def check():
    with open('true.pickle', 'rb') as fp:
        trueboard = list(pickle.load(fp))
    with open('false.pickle', 'rb') as fp:
        falseboard = list(pickle.load(fp))

    for board in trueboard:
        if(winboard.wins(board) == False):
            print("false in true board")

    for board in falseboard:
        if(winboard.wins(board) == True):
            print("true in false board")


def play(player1, player2, width, height, ga, net):

    board = initial_board(width, height)

    player1time = 0
    player2time = 0
    avg = 0

    # print_board(board)
    while True:
        start = time.clock()
        move = player1.move(copy_board(board, width, height))
        end = time.clock()

        trns_board = winboard.translate(board)
        isWin = winboard.wins(trns_board)
        # print(isWin)

        for genome in ga:
            net.putWeights(genome.weights)
            move1 = net.move(board, True)
            print("net: " + str(move1[0]) + " answer: " + str(isWin))
            if (math.fabs(isWin - move1[0]) < 0.01):
                avg +=1

        avg = avg / ga.popSize
        print("avg is: " + str(avg))

        player1time += end - start
        if player1time > 1000:
            print("player 1 out of time")
        if player1time > 10 or not make_move(board, move, width, height):
            return 2  # player 2 has won

#player1.py and player2.py must contain an implemenation of the function move(board)
#which returns a valid move [i,j]
def main():
    start = time.clock()
    numInput, numOutput, numHiddenLayer, neuronPerLayer = 8, 1, 1, 2
    net = NN.NeuralNet(numInput, numOutput, numHiddenLayer, neuronPerLayer)
    # ga = GA.GenAlg()
    with open('ga_tftrain_sig.pickle', 'rb') as fp:
        print(fp.name)
        ga = pickle.load(fp)
    end = time.clock()
    runtime = end - start
    print("init net and GA: " +  str(runtime))

    width = 8   # of board
    height = 8  # of board
    games = 100

    player1wins=0
    for i in range(0,games):
        print("game num: " + str(i))
        start = time.clock()
        if play(player1, player2, width, height, ga, net)==1:
            player1wins+=1
        end = time.clock()
        runtime = end - start
        print("runtime is " + str(runtime))
    # pickle.dump(ga, open('ga-data_step.pickle', 'wb'))

    return 'Player 1 won ' + str(player1wins) + ' out of ' + str(games) + ' games of size '+str(height) + 'x'+str(width)+ '. Total Game Time: '+str(runtime)+' sec'

# train1(50)
# train2(10000)
# train3(10000)
# print (main())
# numInput, numOutput, numHiddenLayer, neuronPerLayer = 2, 1, 1, 3
# net = NN.NeuralNet(numInput, numOutput, numHiddenLayer, neuronPerLayer)
# for i in range(5000):
#     net.train([1.0, 0.0], [1.0])
#     net.train([0.0, 1.0], [1.0])
#     net.train([1.0, 1.0], [0.0])
#     net.train([0.0, 0.0], [0.0])
# print(net.move([1.0, 0.0], True), net.move([0.0, 1.0], True) ,net.move([1.0, 1.0], True), net.move([0.0, 0.0], True))





