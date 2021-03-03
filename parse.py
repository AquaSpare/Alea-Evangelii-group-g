'''
Function that takes the board and create an equivalent GameState object.

Paste this function somwhere in game.py

Be sure to import GameState inside game.py
'''


def parseBoard(board,player):
  gs = GameState()

  if player == Player.BLACK:
    gs.whiteToMove = False

  i = 0
  j = 0
  for row in board:
    j = 0
    for element in row:
      if element == Piece.PAWN:
        gs.board[i][j] = 'wp'
      elif element == Piece.KING:
        gs.board[i][j] = 'wK'
      elif element == Piece.WOLF:
        gs.board[i][j] = 'bp'
      else:
        gs.board[i][j] = '--'
      j+=1
    i+=1

  return gs
