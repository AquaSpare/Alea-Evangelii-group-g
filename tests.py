#!/usr/bin/env python3

import unittest
from game  import *

TEST_BOARD01 = [
#  0123456789ABCDEFGHI
  "  W  W       W  W  ", # 0  
  "                   ", # 1 
  "W    W       W    W", # 2 
  "       W W W       ", # 3 
  "      W P P W      ", # 4 
  "W W  W       W  W W", # 5 
  "    W    P    W    ", # 6 
  "   W    P P    W   ", # 7 
  "    P  P P P  P    ", # 8 
  "   W  P PKP P  W   ", # 9 
  "    P  P P P  P    ", # 10
  "   W    P P    W   ", # 11
  "    W    P    W    ", # 12
  "W W  W       W  W W", # 13
  "      W P P W      ", # 14
  "       W W W       ", # 15
  "W    W       W    W", # 16
  "                   ", # 17
  "  W  W       W  W  ", # 18
]

# For testing capturing of pieces.
TEST_BOARD02 = [
#  0123456789ABCDEFGHI
  " WP          P    P", # 0
  "P    PWP     W    P", # 1
  "W            P    W", # 2
  "                   ", # 3
  "        KWP        ", # 4
  "   WPW             ", # 5
  "             PW    ", # 6
  "                   ", # 7
  "                   ", # 8
  "      W   WP       ", # 9
  "     WP            ", # 10
  "      W            ", # 11
  "                   ", # 12
  "    P        P     ", # 13
  "             W     ", # 14
  "                   ", # 15
  "W                K ", # 16
  "P                WP", # 17
  "W                 W", # 18
]

# For testing capturing of kings.
TEST_BOARD03 = [
#  0123456789ABCDEFGHI
  " KP               P", # 0
  "K       K        WK", # 1
  "W K          W    W", # 2
  "  W     W   WK     ", # 3
  "       WKW         ", # 4
  "              W    ", # 5
  " W KW        PK    ", # 6
  "              W    ", # 7
  "                W  ", # 8
  "      P         K  ", # 9
  "     WKW        W  ", # 10
  "      W       K    ", # 11
  "                   ", # 12
  "     P             ", # 13
  "    PKP            ", # 14
  "        WWW        ", # 15
  "W       WK       W ", # 16
  "K       W W      KW", # 17
  "W                W ", # 18
]

# No black pieces remaining
TEST_BOARD04 = [
#  0123456789ABCDEFGHI
  "                   ", # 0  
  "                   ", # 1 
  "                   ", # 2 
  "                   ", # 3 
  "        P P        ", # 4 
  "                   ", # 5 
  "         P         ", # 6 
  "        P P        ", # 7 
  "    P  P P P  P    ", # 8 
  "      P PKP P      ", # 9 
  "    P  P P P  P    ", # 10
  "        P P        ", # 11
  "         P         ", # 12
  "                   ", # 13
  "        P P        ", # 14
  "                   ", # 15
  "                   ", # 16
  "                   ", # 17
  "                   ", # 18
]

# Black is deadlocked against corner
TEST_BOARD05 = [
#  0123456789ABCDEFGHI
  "                 PW", # 0  
  "                  P", # 1 
  "                   ", # 2 
  "                   ", # 3 
  "                   ", # 4 
  "                   ", # 5 
  "         P         ", # 6 
  "        P P        ", # 7 
  "    P  P P P  P    ", # 8 
  "      P PKP P      ", # 9 
  "    P  P P P  P    ", # 10
  "        P P        ", # 11
  "         P         ", # 12
  "                   ", # 13
  "        P P        ", # 14
  "                   ", # 15
  "                   ", # 16
  "                   ", # 17
  "                   ", # 18
]

# Black is deadlocked at corner and wall
TEST_BOARD06 = [
#  0123456789ABCDEFGHI
  "       PWP       PW", # 0  
  "        P         P", # 1 
  "                   ", # 2 
  "                   ", # 3 
  "                   ", # 4 
  "                   ", # 5 
  "         P         ", # 6 
  "        P P        ", # 7 
  "    P  P P P  P    ", # 8 
  "      P PKP P      ", # 9 
  "    P  P P P  P    ", # 10
  "        P P        ", # 11
  "         P         ", # 12
  "                   ", # 13
  "        P P        ", # 14
  "                   ", # 15
  "                   ", # 16
  "                   ", # 17
  "                   ", # 18
]

# White has both its king and a pawn deadlocked
TEST_BOARD07 = [
#  0123456789ABCDEFGHI
  "       WKW         ", # 0  
  "       WPW         ", # 1 
  "        W          ", # 2 
  "                   ", # 3 
  "                   ", # 4 
  "                   ", # 5 
  "                   ", # 6 
  "                   ", # 7 
  "                   ", # 8 
  "                   ", # 9 
  "                   ", # 10
  "                   ", # 11
  "                   ", # 12
  "                   ", # 13
  "                   ", # 14
  "                   ", # 15
  "                   ", # 16
  "                   ", # 17
  "                   ", # 18
]


def convert(c):
  if c == ' ':
    return Piece.NONE
  elif c == 'P':
    return Piece.PAWN
  elif c == 'W':
    return Piece.WOLF
  elif c == 'K':
    return Piece.KING
  else:
    raise ValueError("Only supports characters ' ', 'P', 'W', and 'K'.")

# Allows easy construction of boards for tests.
def parseTestBoard(b):
  board = []
  for row in b:
    board.append([convert(p) for p in row])
  return board
    

# Add tests by defining methods as 'test_<function_to_test>'
# and use asserts provided by the unittest module.
# Run using './tests.py' or 'python3 -m unittest tests'.
class TestGameMethods(unittest.TestCase):

  def test_nextPlayer(self):
    playerOne = Player.WHITE
    playerTwo = Player.BLACK
    self.assertEqual(nextPlayer(playerOne), playerTwo)
    self.assertEqual(nextPlayer(playerTwo), playerOne)

  def test_movePiece(self):
    # Moves a piece around in the board and asserts that the board is updated
    # accordingly.
    board = parseTestBoard(TEST_BOARD01)
    positions = [
        Position(0,2),
        Position(0,3),
        Position(6,3),
        Position(6,1),
        Position(0,1),
        Position(0,2)
    ]
    for i in range(len(positions)-1):
      pos1, pos2 = positions[i], positions[i+1]
      piece = getBoardPiece(board, pos1)
      move = (pos1, pos2)
      p = movePiece(board, move)
      self.assertEqual(p, piece) # returns moved piece
      self.assertEqual(getBoardPiece(board, pos1), Piece.NONE) # old pos updated
      self.assertEqual(getBoardPiece(board, pos2), piece) # new pos updated

  def test_tryCapturePiece(self):
    cases = {
      (Position(0,1),   Position(0,0),   Player.WHITE),  # With marked square horizontally.
      (Position(1,0),   Position(2,0),   Player.BLACK),  # With marked square vertically.
      (Position(1,6),   Position(1,5),   Player.WHITE),  # With surrounding pieces horizontally.
      (Position(1,6),   Position(1,7),   Player.WHITE),  # With surrounding pieces horizontally.
      (Position(1,13),  Position(0,13),  Player.WHITE),  # With surrounding pieces vertically.
      (Position(1,13),  Position(2,13),  Player.WHITE),  # With surrounding pieces vertically.
      (Position(1,18),  Position(2,18),  Player.BLACK),  # With blocked marked square.
      (Position(4,9),   Position(4,8),   Player.WHITE),  # With king and pawn.
      (Position(4,9),   Position(4,10),  Player.WHITE),  # With king and pawn.
      (Position(5,4),   Position(5,3),   Player.BLACK),  # With surrounding pieces horizontally.
      (Position(5,4),   Position(5,5),   Player.BLACK),  # With surrounding pieces horizontally.
      (Position(9,10),  Position(9,11),  Player.WHITE),  # With middle marked square.
      (Position(10,6),  Position(9,6),   Player.BLACK),  # With three surrounding.
      (Position(10,6),  Position(11,6),  Player.BLACK),  # With three surrounding.
      (Position(17,0),  Position(16,0),  Player.BLACK),  # With marked and surrounding.
      (Position(17,0),  Position(18,0),  Player.BLACK),  # With marked and surrounding.
      (Position(17,17), Position(16,17), Player.WHITE),  # With king and mark.
    }

    for mid,opp,player in cases:
      # All positions above should be captured.
      board = parseTestBoard(TEST_BOARD02)
      if player == Player.BLACK:
        capturers = {Piece.WOLF}
        opponents = {Piece.PAWN}
        piece = Piece.PAWN
      else:
        capturers = {Piece.PAWN, Piece.KING}
        opponents = {Piece.WOLF}
        piece = Piece.WOLF
      self.assertEqual(tryCapturePiece(board, capturers, opponents, mid, opp),
                       piece,
                      "With positions {}, {}".format(str(mid), str(opp))) 
      self.assertEqual(getBoardPiece(board, mid), Piece.NONE, "With position {}".format(str(mid)))

  def test_tryCaptureKing(self):
    board = parseTestBoard(TEST_BOARD03)
    positions = {Position(r,c) for r in range(BOARD_BOUNDARY) for c in range(BOARD_BOUNDARY)}
    capturedPositions = {
      Position(1,0),   # With two marked squares.
      Position(1,18),  # With one "blocked" marked square.
      Position(4,8),   # With three wolves.
      Position(10,6),  # With three wolves and pawn.
      Position(17,0),  # With one marked.
      Position(17,17), # With three wolves and marked.
    }

    for pos in capturedPositions:
      # All king positions above should be captured.
      self.assertTrue(tryCaptureKing(board, pos), "With position {}".format(str(pos))) 
      self.assertEqual(getBoardPiece(board, pos), Piece.NONE, "With position {}".format(str(pos)))

    for pos in positions:
      # All other king positions should not be captured.
      piece = getBoardPiece(board, pos)
      if piece == Piece.KING:
        self.assertFalse(tryCaptureKing(board, pos), "With position {}".format(str(pos)))
        self.assertEqual(getBoardPiece(board, pos), piece, "With position {}".format(str(pos)))

  def test_checkForWin(self):
    cases = [
      (Player.BLACK, [Piece.KING], Piece.WOLF, Position(3,2), True),
      (Player.BLACK, [Piece.PAWN, Piece.KING], Piece.WOLF, Position(6,1), True),
      (Player.BLACK, [Piece.PAWN, Piece.KING], Piece.WOLF, Position(1,8), True),
      (Player.BLACK, [Piece.PAWN, Piece.KING, Piece.PAWN], Piece.WOLF, Position(1,10), True), 
      (Player.BLACK, [], Piece.WOLF, Position(1,12), False), 
      (Player.BLACK, [Piece.PAWN, Piece.PAWN], Piece.WOLF, Position(1,12), False), 
      (Player.WHITE, [Piece.WOLF, Piece.WOLF], Piece.PAWN, Position(0,0), False), 
      (Player.WHITE, [], Piece.PAWN, Position(18,17), False),
      (Player.WHITE, [], Piece.PAWN, Position(9,10), False), 
      (Player.WHITE, [], Piece.KING, Position(0,1), True), 
      (Player.WHITE, [Piece.WOLF], Piece.KING, Position(0,17), True), 
      (Player.WHITE, [], Piece.KING, Position(0,18), True), 
      (Player.WHITE, [], Piece.KING, Position(18,18), True), 
      (Player.WHITE, [Piece.WOLF], Piece.KING, Position(18,18), True), 
      (Player.WHITE, [Piece.WOLF], Piece.KING, Position(7,0), False), 
      (Player.WHITE, [Piece.WOLF], Piece.KING, Position(2,0), False), 
      (Player.WHITE, [], Piece.KING, Position(9,9), False), 
    ]
    for player, capturedPieces, movedPiece, pos, expected in cases:
      self.assertEqual(expected, checkForWin(player, capturedPieces, movedPiece, pos))

  def test_isValidInput(self):
    invalidInputs = [""," ", "a20", "a-1", "a0", "a111", "a!1"]
    for square in invalidInputs:
      self.assertFalse(isValidInput(square))
    
    validInputs = ["a1","A1", "s19", "S19"]
    for square in validInputs:
      self.assertTrue(isValidInput(square))

  def test_isValidMove(self):
    player = Player.WHITE
    board = parseTestBoard(TEST_BOARD01)

    blockedPath = ("O11", "O14") # another piece is in the path
    diagonal = ("O11", "M9") # moving diagonally
    occupied = ("O11", "L11") # moving to an occupied square
    kingTooFar = ("J10", "E15") # king is moving more than 4 squares
    notSupportedMove = ("H11", "F12") #pawn moving non-perfect-vertical,horizontal or diagonal
    kingNotSupportedMove = ("J10", "H11") #king moving non-perfect-vertical,horizontal or diagonal
    
    illegalMoves = [blockedPath, diagonal, occupied, kingTooFar, notSupportedMove, kingNotSupportedMove]
    for move in illegalMoves:
      self.assertFalse(isValidMove(board, player, move))

    west = ("K5", "K1")
    east = ("K15", "K19")
    north = ("E9", "A9")
    south = ("O9", "S9")
    diagonalKingLegal = ("J10", "G13")
    legalMoves = [west, east, north, south, diagonalKingLegal]
    for move in legalMoves:
      self.assertTrue(isValidMove(board, player, move))

  def test_parseMove(self):
    self.assertEqual(parseMove("A1"), Position(0,0))
    self.assertEqual(parseMove("S19"), Position(18,18))
    self.assertEqual(parseMove("a1"), parseMove("A1"))
    self.assertEqual(parseMove("S19"), parseMove("s19"))

  def test_isOwnPiece(self):
    #player WHITE
    player = Player.WHITE
    board = parseTestBoard(TEST_BOARD01)
    self.assertTrue(isOwnPiece(player, board, "o11")) #PAWN
    self.assertTrue(isOwnPiece(player, board, "j10")) #KING
    self.assertFalse(isOwnPiece(player, board, "A1")) #NONE

    #player BLACK
    player = Player.BLACK
    self.assertTrue(isOwnPiece(player, board, "q6")) #WAREWOLF
    self.assertFalse(isOwnPiece(player, board, "A1")) #NONE

  def test_isDeadlock(self):
    #Black has no remaining pieces
    captured = {Player.WHITE: 0, Player.BLACK: BLACK_PIECES}
    player = Player.BLACK
    boardNoBlack = parseTestBoard(TEST_BOARD04)
    self.assertTrue(isDeadlock(boardNoBlack, player, captured))

    #Black has one remaining and is cornered and deadlocked
    captured = {Player.WHITE: 0, Player.BLACK: BLACK_PIECES - 1}
    boardBlackDeadlock = parseTestBoard(TEST_BOARD05)
    self.assertTrue(isDeadlock(boardBlackDeadlock, player, captured))

    #Black has two remaining and both are cornered and deadlocked
    captured = {Player.WHITE: 0, Player.BLACK: BLACK_PIECES - 2}
    boardBlackDeadlock = parseTestBoard(TEST_BOARD06)
    self.assertTrue(isDeadlock(boardBlackDeadlock, player, captured))

    #White has managed to deadlock both the remaining pawn and king
    player = Player.WHITE
    captured = {Player.WHITE: WHITE_PIECES - 2, Player.BLACK: BLACK_PIECES - 5}
    boardWhiteDeadlock = parseTestBoard(TEST_BOARD07)
    self.assertTrue(isDeadlock(boardWhiteDeadlock, player, captured))


if __name__ == '__main__':
    unittest.main()
