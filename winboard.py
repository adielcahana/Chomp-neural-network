#http://stackoverflow.com/questions/6831502/algorithm-for-the-game-of-chomp
import time
import pickle
from functools import wraps
import atexit

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

def detranslate(trns_board , board):
    for i in range (0,len(board)):
        for j in range (0,len(board[0])):
            if (i,j) not in trns_board:
                board[i][j] = 0

# computes list of boards reachable in one move.
def moves(board):
    return [frozenset([(x,y) for (x,y) in board if x < px or y < py]) for (px,py) in board]

# def memoize(f):
# # http: // stackoverflow.com / questions / 16463582 / memoize - to - disk - python - persistent - memoization
#   class memodict(dict):
#       __slots__ = ()
#       def __missing__(self, key):
#           self[key] = ret = f(key)
#           return ret
#   try:
#       memo = pickle.load(open("memo.pickle", 'rb'))
#   except (IOError, ValueError):
#       memo = memodict()
#
#   atexit.register(lambda: pickle.dump(memo, open("memo.pickle", 'wb')))
#   return memo.__getitem__
class memodict(dict):
    # __slots__ = ()
    def __init__(self, f):
        super.__init__(super())
        self.f = f
    def __missing__(self, key):
        self[key] = ret = self.func(key)
        return ret

def memoize(f):
  class memodict(dict):
      __slots__ = ()
      def __missing__(self, key):
          self[key] = ret = f(key)
          return ret
  #   try:
  #       memo = pickle.load(open("memo.pickle", 'rb'))
  #   except (IOError, ValueError):
  #       memo = memodict(f)

    # atexit.register(lambda: pickle.dump(memo, open("memo.pickle", 'wb')))
    # return memo.__getitem__
  return memodict().__getitem__

# computes whether the board is a winning position
@memoize
def wins(board):
    if not board:
        return True
    return any(not wins(move) for move in moves(board))

def show(board):
    for x in range(8):
        print( '|' + ''.join('x ' if (x,y) in board else '  ' for y in range(8)))

# n,m = 7,7
# init = frozenset((x,y) for x in range(n) for y in range(m))
# print(wins(init))
