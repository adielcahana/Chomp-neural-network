import numpy as np
import pickle
# from sklearn import svm
from sklearn import linear_model
import random
import neuralNet as NN
import training as trn
import winboard
with open('true.pickle', 'rb') as fp:
    trueboard = list(pickle.load(fp))
with open('false.pickle', 'rb') as fp:
    falseboard = list(pickle.load(fp))
nn = NN.NeuralNet(0,0,0,0)
model = linear_model.Perceptron(penalty=None, alpha=0.0001, fit_intercept=True, n_iter=5, shuffle=True, verbose=0, eta0=1.0, n_jobs=1, random_state=0, class_weight=None, warm_start=False)
# with open('model.pickle', 'rb') as fp:
#     model = pickle.load(fp)


boards = []
tag = []
width, height = 8 ,8
i=0
for board in trueboard:
    if i > 2*len(falseboard):
        break
    b = trn.initial_board(width, height)
    winboard.detranslate(board, b)
    boards.append(tuple([nn.translate(b), 1]))
    i+=1

for board in falseboard:
    b = trn.initial_board(width, height)
    winboard.detranslate(board, b)
    boards.append(tuple([nn.translate(b),-1]))

new_boards = []
new_tag = []
np.random.shuffle(boards)
for (board,tag) in boards:
    new_boards.append(np.array(board))
    new_tag.append(tag)

model.fit(new_boards, new_tag)
print(model.score(new_boards, new_tag))

#Predict Output
trueboards = random.sample(trueboard, 100)
falseboards = random.sample(falseboard, 100)

boards = []

for i in range(100):
    tb = trn.initial_board(width, height)
    fb = trn.initial_board(width, height)
    winboard.detranslate(trueboards[i], tb)
    winboard.detranslate(falseboards[i], fb)
    boards.append(np.array(nn.translate(tb)))
    boards.append(np.array(nn.translate(fb)))

boards = np.array(boards)
predicted = model.predict(boards)
expected = [(-1)**(i % 2) for i in range(len(boards))]

avg = 0
for i in range(len(boards)):
    if predicted[i] == expected[i]:
        avg += 1
print(avg/len(boards))
# pickle.dump(model, open('model.pickle', 'wb'))



