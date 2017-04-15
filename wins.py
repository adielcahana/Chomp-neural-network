import winboard
import training
import pickle, json
import atexit

def memoize(f):
# http: // stackoverflow.com / questions / 16463582 / memoize - to - disk - python - persistent - memoization
  class memodict(dict):
      __slots__ = ()
      def __missing__(self, key):
          self[key] = ret = f(key)
          return ret
  try:
      memo = pickle.load(open("memo.pickle", 'rb'))
  except (IOError, ValueError):
      memo = memodict()

  atexit.register(lambda: pickle.dump(memo, open("memo.pickle", 'wb')))
  return memo.__getitem__

# computes whether the board is a winning position
@memoize
def wins(board):
    if not board[0]:
        return True
    return any(not wins(move) for move in [move(board, mov) for mov in moves(board)])

#return a board after the move
def move(board, move):
    new_board = []
    for i in range(0, move[0]):
        new_board.append(board[i])
    for i in range(move[0], len(board)):
        if board[i] <= move[1]:
            new_board.extend([board[i] * (len(board) - i)])
            return tuple(new_board)
        else: new_board.append(move[1])
    return tuple(new_board)

#returns all moves posible in board
def moves(board):
    moves= []
    for i in range(len(board)):
        if board[i] > 0:
            moves.extend([[i,j] for j in range(board[i])])
        else: break
    return moves

def show(board):
    print(" " + ''.join('_ ' for y in range(board[0])))
    for x in range(len(board)):
        print( '|' + ''.join('x ' for y in range(board[x])))

def translate(board):
    trns_board = []
    sum = 0
    new_board = training.initial_board(8,8)
    winboard.detranslate(board, new_board)
    for raw in new_board:
        for x in raw:
            if x == 0: break
            sum += x
        trns_board.append(sum)
        sum = 0
    return tuple(trns_board)


init = tuple([8] * 8)
print(wins(init))


# with open('false.pickle', 'rb') as fp:
#     falseboard = list(pickle.load(fp))
#
# for fb in falseboard:
#     init = translate(fb)
#     show(init)
#     print(init)
#     print(wins(init))
#     winboard.show(fb)
#     print(winboard.wins(fb))
#     print()

