import chess
import sys

print(sys.argv)
with open(sys.argv[1]) as infile:
  for line in infile:
    board = chess.Board(fen=line)
    print(board)
    input()
