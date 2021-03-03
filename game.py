#!/usr/bin/env python3

"""A game platform to play a terminal-based Alea Evangelii.

Allows players to play a game of Alea Evangelii, an ancient religious board
game between two players. The game is played as local multiplayer with a
terminal-based interface.
"""

from enum import Enum
from itertools import zip_longest
import string
import re
from GameEngine import GameState
from gameAI import computerMove

# ---- Classes ---------------------------------------------
class Mode(Enum):
  HUMANW_VS_AIB = "Human(White) vs AI(Black)"
  HUMANB_VS_AIW = "Human(Black) vs AI(White)"
  AI_VS_AI = "AI vs AI"
  HUMAN_VS_HUMAN = "Human vs Human"

class Player(Enum):
  """An enumarable for players.
  """
  WHITE = "White"
  BLACK = "Black"

class Piece(Enum):
  """An enumarable for the possible pieces placed in squares in the board (or
  absence thereof).
  """
  KING = '⛃'
  PAWN = '⛂'
  WOLF = '⛀'
  NONE = ' '

class Position:
  """A class representing a position (square) of the board.

  A position (square) of the board is identified by a row and column that can be
  used to index a piece of the underlying board representation.

  Attributes:
    r: The row identifier.
    c: The column identifier.
  """
  def __init__(self, r, c):
    """Constructor for Position objects.

    Args:
      r: A row identifier.
      c: A column identifier.

    Raises:
      ValueError: If arguments are not valid rows or columns.
    
    Returns:
      A new position object.
    """
    if r < 0 or r > BOARD_BOUNDARY or c < 0 or c > BOARD_BOUNDARY:
      raise ValueError("A postion must only hold valid board indices.")
    self.r = r
    self.c = c

  def __eq__(self, other):
    """Equality comparison for Position objects.

    Args:
      other: The object to compare against.
    
    Returns:
      True if both positions identify the same square; False otherwise.
    """
    return isinstance(other, self.__class__) and self.r == other.r and self.c == other.c

  def __hash__(self):
    """Hash function for Position objects.
    
    Returns:
      A hash for the object.
    """
    return hash((self.r, self.c))

  def __str__(self):
    """Convert a Position object to a string representation.
    
    Returns:
      A string representing the position in the form '(r, c)'.
    """
    return "({},{})".format(self.r, self.c)

  def adjacent(self):
    """Fetch all adjacent positions.

    Returns:
      A list of Position objects adjacent to the object.
    """
    return [pos for pos in [self.up(), self.down(), self.left(), self.right()] if pos is not None]

  def up(self):
    """Fetch the position above the object.

    Returns:
      A position object for the position above the original object; or None if
      there is no such position.
    """
    try:
      return Position(self.r-1, self.c)
    except ValueError:
      return None

  def down(self):
    """Fetch the position below the object.

    Returns:
      A position object for the position below the original object; or None if
      there is no such position.
    """
    try:
      return Position(self.r+1, self.c)
    except ValueError:
      return None

  def right(self):
    """Fetch the position to the right of the object.

    Returns:
      A position object for the position to the right of the original object;
      or None if there is no such position.
    """
    try:
      return Position(self.r, self.c+1)
    except ValueError:
      return None

  def left(self):
    """Fetch the position to the left of the object.

    Returns:
      A position object for the position to the left of the original object; or
      None if there is no such position.
    """
    try:
      return Position(self.r, self.c-1)
    except ValueError:
      return None

  def isMarked(self):
    """Check if the position is a marked position.

    Returns:
      True if the position is a marked position; False otherwise.
    """
    return (self.r, self.c) in MARKED_POSITIONS

  def isMarkedCorner(self):
    """Check if the position is a marked corner position.

    Returns:
      True if the position is a marked corner position; False otherwise.
    """
    return (self.r, self.c) in MARKED_POSITIONS and (self.r, self.c) != MIDDLE_POSITION


# ---- Integration ---------------------------------------
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

# ---- Functionality ---------------------------------------

def playGame(startParams):
  """Play a game of Alea Evangelii.
  """
  mode, playerOne, playerTwo = startParams
  board = INITIAL_BOARD
  player = playerOne
  captured = {playerOne: 0, playerTwo: 0}
  hasWon = False

  while not hasWon:
    player = nextPlayer(player)
    printBoard(board, player, captured)
    gs = parseBoard(board,player)
    move = computerMove(gs,'hard')
    
    if(not isDeadlock(board, player, captured)):
      move = getMove(board, player, mode)
      toPos = move[1]
      movedPiece = movePiece(board, move)
      capturedPieces = capturePieces(board, player, movedPiece, toPos)
      captured[player] += len(capturedPieces)
      hasWon = checkForWin(player, capturedPieces, movedPiece, toPos)

  printBoard(board, player, captured)
  print("{} has won!".format(player.value))

def nextPlayer(player):
  """Get the next player in turn.

  Args:
    player: The player who's turn it currently is.

  Returns:
    The next player to take a turn.
  """
  if player == Player.BLACK:
    return Player.WHITE
  else:
    return Player.BLACK

def getInput(board, player):
  """Gets and validates the input from user.

  Gets a position on the board, i.e. 'A1', as input from player and validates
  that the position exists and contains a piece belonging to the player. Gets
  another position on the board, i.e. 'A2', as input from player and validates
  that the position exists.

  Args:
    board: The board used to confirm if a piece belongs to the player.
    player: Current player to input their move.

  Returns: 
    A tuple of string represenation of positions on the board of type (str,str).
  """
  origin = input("Move piece from: ")
  while(not isValidInput(origin) or not isOwnPiece(player, board, origin)):
    origin = input("Move piece from: ")
  
  to = input("Move piece to:   ")
  while(not isValidInput(to)):
    to = input("Move piece to:   ")

  move = (origin, to)
  return move

#DUMMY FUNCTION, REPLACE WITH MOVE FROM ACTUAL AI
def getInputFromAI(board, player):
  print("Getting input from AI, test")
  return getInput(board, player)

def getMove(board, player, mode):
  """Gets and validates a move input by a player OR ai.

  Gets a move (as in a start position and an end position on the board), and
  checks if the move is valid according to game rules.

  Args:
    board: The game board.
    player: Current player to input their move.

  Returns: 
    A tuple of positions on the board of type (Position,Position).
  """
  if(mode == Mode.HUMAN_VS_HUMAN or 
  (mode == Mode.HUMANB_VS_AIW and player == Player.BLACK) or 
  (mode == Mode.HUMANW_VS_AIB and player == Player.WHITE)):
    
    move = getInput(board, player)
    
    while(not isValidMove(board, player, move)):
      move = getInput(board, player)
    
    positionStart, positionEnd = move
    return (parseMove(positionStart), parseMove(positionEnd))

  else:
    move = getInputFromAI(board, player)
    
    while(not isValidMove(board, player, move)):
      move = getInputFromAI(board, player)
    
    positionStart, positionEnd = move
    return (parseMove(positionStart), parseMove(positionEnd))


def parseMove(square):
  """Extract row and column indexes from a user input.

  Args:
    square: The string representation of a position on the board, i.e. 'A1' of type str.

  Returns: 
    A zero-indexed position on the board of type Position.
  """
  row = string.ascii_lowercase.index(square[0].lower())
  column = int(square[1] + square[2]) if len(square) == 3 else int(square[1])

  return (Position(row, column - 1))

def isValidInput(square):
  """Check if a string representation of a position on the board is of correct
  format and in range.

  Args:
    square: The string representation of a position on the board, i.e. 'A1' of
            type str.

  Returns: 
    True if arg is of correct format and in range of the board, else False.
  """
  #Check if input is in format A1-S19
  if(not (re.fullmatch("[a-sA-S][1][0-9]", square) or re.fullmatch("[a-sA-S][1-9]", square))):
    print("Please use the correct input format, [a1-s19], [A1-S19]")
    return False

  #If we reach here, no bad input has been detected.
  return True

def isPathClearRow(board, positions):
  """Check if the path of a move on a row is clear.

  Args:
    board: The board to be searched.
    positions: A tuple of the start- and end positions of the move, type (Position, Position).

  Returns: 
    True if no piece blocks the path of the move, else False.
  """
  posOrigin, posTo = positions
  incOrDec = -1 if (posTo.c - posOrigin.c < 0) else 1
  row = board[posOrigin.r]
  for square in range(posOrigin.c + incOrDec, posTo.c, incOrDec):
    if(row[square] != Piece.NONE):
      return False
  return True

def isPathClearColumn(board, positions):
  """Check if the path of a move on a column is clear.

  Args:
    board: The board to be searched.
    positions: A tuple of the start- and end positions of the move, type (Position, Position).

  Returns: 
    True if no piece blocks the path of the move, else False.
  """
  posOrigin, posTo = positions
  incOrDec = -1 if (posTo.r - posOrigin.r < 0) else 1
  column = posOrigin.c
  for row in range(posOrigin.r + incOrDec, posTo.r, incOrDec):
    if(board[row][column] != Piece.NONE):
      return False
  return True

def isPathClearDiagonal(board, positions):
  """Check if the path of a move on a diagonal is clear.

  Args:
    board: The board to be searched.
    positions: A tuple of the start- and end positions of the move, type (Position, Position).

  Returns: 
    True if no piece blocks the path of the move, else False.
  """
  posOrigin, posTo = positions
  columnIncOrDec = -1 if (posTo.c - posOrigin.c < 0) else 1
  rowIncOrDec = -1 if (posTo.r - posOrigin.r < 0) else 1
  for row, column in zip(range(posOrigin.r + rowIncOrDec , posTo.r, rowIncOrDec), range(posOrigin.c + columnIncOrDec, posTo.c, columnIncOrDec)):
    if(board[row][column] != Piece.NONE):
      return False
  return True

def nrOfSquaresBetweenPositions(positions):
  """Counts the number of squares between two positions. Only makes sense if the path between the two positions is
      on a perfect vertical, horizontal or diagonal.

  Args:
    positions: A tuple of the start- and end positions of the move, type (Position, Position).

  Returns:
    The number, of type int, of squares between one position and another.
  """
  posOrigin, posTo = positions
  if(posOrigin.r == posTo.r):
    return abs(posTo.r - posOrigin.r)
  elif(posOrigin.c == posTo.c):
    return abs(posTo.c - posOrigin.c)
  else:
    return abs(posTo.c - posOrigin.c)

def isValidMove(board, player, move):
  """Check if a move is legal.

  Args:
    board: The board to be searched.
    player: The player inputing the move.
    move: A tuple of start position and end position of type (str, str), i.e ("A1", "A2").

  Returns: 
    True if the move is legal, else False.
  """
  (origin, to) = move
  posOrigin = parseMove(origin)
  posTo = parseMove(to)

  #If player is moving the king, it cannot move more than 4 squares
  if(board[posOrigin.r][posOrigin.c] == Piece.KING):
    if(nrOfSquaresBetweenPositions((posOrigin,posTo)) > 4):
      print("The king cannot traverse more than 4 squares at once.")
      return False

  #If player is making a move on a perfect vertical
  if(posOrigin.r == posTo.r):
    if(not isPathClearRow(board,(posOrigin,posTo))):
      print("A piece is in your path, try another path.")
      return False
    
  #If player is making a move on a perfect horizontal
  elif(posOrigin.c == posTo.c):
    if(not isPathClearColumn(board,(posOrigin,posTo))):
      print("A piece is in your path, try another path.")
      return False

  #If player is making a move which is on a perfect diagonal
  elif(abs(posOrigin.c - posTo.c) == abs(posOrigin.r - posTo.r)):
    if(board[posOrigin.r][posOrigin.c] != Piece.KING):
      print("Only the king may move diagonally.")
      return False
    else:
      if(not isPathClearDiagonal(board,(posOrigin,posTo))):
        print("A piece is in your path, try another path.")
        return False

  #Only possibility left is that player is making a move 
  #which is not a perfect vertical, horizontal, diagonal
  else:
    print("That move is not vertical, horizontal or diagonal. Try another move.")
    return False

  #Check if the square moved to is occupied
  if(board[posTo.r][posTo.c] != Piece.NONE):
    print("You are trying to move to an occupied square.")
    return False
  
  return True

def isOwnPiece(player, board, square):
  """Checks if a position contains a piece belonging to the player.

  Args:
    player: The player.
    board: The board to searched.
    square: String representation of a position on the board, i.e. 'A1'.

  Returns: 
    True if the square contains a piece belonging to the player, else False.
  """
  position = parseMove(square)
  piece = board[position.r][position.c]
  if piece == Piece.NONE:
    print("The square is empty.")
    return False
  elif player == Player.BLACK:
    if piece != Piece.WOLF:
      print("That piece does not belong to you.")
      return False
  else:
    if piece != Piece.PAWN and piece != Piece.KING:
      print("That piece does not belong to you.")
      return False

  return True

def isDeadlock(board, player, captured):
  """Checks if the current player can make a move or not.
  A player cannot make a move if none of its pieces has an adjacent empty position to move to.

  Args:
    board: The board to be searched.
    player: The current player.
    captured: The number of captured white and black pieces.

  Returns: 
    True if there is a deadlock, else false.
  """
  if(player == Player.BLACK and captured[Player.BLACK] == BLACK_PIECES):
    print("Black has no remaining pieces. Skipping to white's turn.")
    return True
  
  for row in range(0,BOARD_BOUNDARY):
    for column in range(0,BOARD_BOUNDARY):
      position = Position(row,column)
      piece = getBoardPiece(board, position)
      if(player == Player.WHITE and (piece == Piece.PAWN or piece == Piece.KING)):
        if(isAdjacentNone(position, board)):
          return False  
      elif(player == Player.BLACK and piece == Piece.WOLF):
        if(isAdjacentNone(position, board)):
          return False

  #Deadlock
  print(("Black" if player == Player.BLACK else "White") +" is in a deadlock position. Skipping its turn.")
  return True

def isAdjacentNone(position, board):
  """Checks if any adjacent positions to a specific position are empty.

  Args:
    board: The board to searched.
    position: A position on the board of type Position.

  Returns: 
    True if the position has any adjacent empty positions.
  """
  adjacentPositions = position.adjacent()
  for adjacentPosition in adjacentPositions:
    if getBoardPiece(board, adjacentPosition) == Piece.NONE:
      return True
  return False


def movePiece(board, move):
  """Moves a piece in the board.

  Moves a piece according to move in the board. Expects move to be a valid move, obeying game rules and is withing board boundaries. Gives the type of piece that was moved.

  Args:
    board: The board to be updated.
    move: A tuple of positions, the first being the position to move from; the
           second the position to move to.

  Returns: 
    The type of piece that was moved (of type Piece).
  """
  src, end  = move
  assert board[src.r][src.c] != Piece.NONE
  assert board[end.r][end.c] == Piece.NONE
  piece = getBoardPiece(board, src)
  setBoardPiece(board, end, piece)
  setBoardPiece(board, src, Piece.NONE)
  return piece


def setBoardPiece(board, pos, piece):
  """Set the piece in a specific square of the board.

  Args:
    board: The board to be updated.
    pos: The position of the square to update.
    piece: The piece to put inside the square.
  """
  board[pos.r][pos.c] = piece

def getBoardPiece(board, pos):
  """Fetch the piece in a specific square of the board.

  Args:
    board: The board to be fetched from.
    pos: The position of the square to fetch from.

  Returns:
    The type of piece residing on position pos in board.
  """
  return board[pos.r][pos.c]

def capturePieces(board, player, movedPiece, pos):
  """Attempt to capture pieces.

  Removes any pieces captured as a result of the previous move from the board.

  Args:
    board: The board to be updated.
    player: The player who took the turn.
    movedPiece: The piece that was moved in the turn.
    pos: To position to which the movedPiece was moved.

  Returns:
    A list of pieces that were captured.
  """
  captured = []

  if player == Player.BLACK:
    capturers = {Piece.WOLF}
    opponents = {Piece.PAWN}
  else:
    capturers = {Piece.PAWN, Piece.KING}
    opponents = {Piece.WOLF}

  
  l = pos.left()
  r = pos.right()
  u = pos.up()
  d = pos.down()

  ll = l.left()  if l is not None else None
  rr = r.right() if r is not None else None
  uu = u.up()    if u is not None else None
  dd = d.down()  if d is not None else None

  pairs = [
    (l, ll),
    (r, rr),
    (u, uu),
    (d, dd),
  ]

  for middle, opposite in pairs:
    if middle is not None and opposite is not None:
      if player == Player.BLACK and getBoardPiece(board, middle) == Piece.KING:
        wasCaptured = tryCaptureKing(board, middle)
        if wasCaptured:
          captured.append(Piece.KING)
      else:
        capturedPiece = tryCapturePiece(board, capturers, opponents, middle, opposite)
        if capturedPiece is not None:
          captured.append(capturedPiece)

  return captured

def tryCapturePiece(board, capturers, opponents, middle, opposite):
  """Attempt to capture a piece.

  Checks whether or not the piece residing on position pos in the board has been
  captured; if so, it is removed from the board. 

  If the piece to be captured is a king, this function will not capture it, as
  different rules apply. See tryCaptureKing() instead.

  Args:
    board: The board.
    capturers: A list of pieces that can be part of the capture.
    opponents: A list of pieces that can be captured.
    middle: The position of the piece possibly captured. 
    opposite: The position next to middle, opposite of the position of the
              capturing invoker.
  Returns:
    The piece in position middle that was captured, or None if no piece was
    captured.
  """
  captured = None
  isOpponent = getBoardPiece(board, middle) in opponents
  isCapturer = getBoardPiece(board, opposite) in capturers or opposite.isMarked()

  if isOpponent and isCapturer:
    captured = getBoardPiece(board, middle)
    setBoardPiece(board, middle, Piece.NONE)

  return captured

def tryCaptureKing(board, pos):
  """Attempt to capture a king.

  Checks whether or not the king residing on position pos in the board has been
  captured; if so, it is removed from the board. A king is captured if it is
  surrounded by three werewolves (Piece.WOLF) and/or marked squares.

  Args:
    board: The board.
    pos: The position of the king.

  Returns:
    True if the king was captured; False otherwise.
  """
  assert getBoardPiece(board, pos) == Piece.KING

  surr = 0
  for adj in pos.adjacent():
    if adj.isMarked() or getBoardPiece(board, adj) == Piece.WOLF:
      surr += 1
  if surr >= 3:
    setBoardPiece(board, pos, Piece.NONE)
    return True
  return False

def checkForWin(player, capturedPieces, movedPiece, pos):
  """Check if the game has been won.

  Game is won if black player has captured the king or if white player has
  moved the king to a marked corner square.

  Args:
    player: The player who took the last turn.
    capturedPieces: The pieces captured in the turn.
    movedPiece: The piece that was moved in the turn.
    pos: The position to which the movedPiece was moved.

  Returns:
    True if the game is won; False otherwise.
  """
  if player == Player.BLACK and Piece.KING in capturedPieces:
    return True
  if player == Player.WHITE and movedPiece == Piece.KING and pos.isMarkedCorner():
    return True
  return False

def printBoard(board, player, captured):
  """Prints a board in a grid-like fashion, alongside help and status text.

  Args:
    board: The internal board representation to be pretty printed.
    player: The player who is next to play.
    captured: A dict indexable by both Player-values storing the amount of
              captured pieces by each player respectively.
  """
  top = "  ┌" + "┬".join(["─"*3]*19) + "┐\n"
  mid = "  ├" + "┼".join(["─"*3]*19) + "┤\n"
  bot  = "  └─⌃─┴─⌃─┴" + "┴".join(["─"*3]*15) + "┴─⌃─┴─⌃─┘\n"
  specialMidSides  = "  ├─⌃─┼─⌃─┼" + "┼".join(["─"*3]*15) + "┼─⌃─┼─⌃─┤\n"
  specialMidCenter = "  ├" + "┼".join(["─"*3]*9) + "┼─⌃─┼" + "┼".join(["─"*3]*9) + "┤\n"

  numbers = "   " + " ".join('{:^3}'.format(d) for d in range(1,20))

  drawing = top
  for c, row in enumerate(board):
    drawing += chr(c + 65) 
    drawing += " │" 
    drawing += "│".join('{:^3}'.format(sq.value) for sq in row) 
    drawing += "│\n" 
    if c < 2 or c == 17:
      drawing += specialMidSides
    elif c == 9:
      drawing += specialMidCenter
    elif c < 18:
      drawing += mid

  drawing += bot
  drawing += numbers

  status = [
    "Black has captured {} pieces.".format(captured[Player.BLACK]),
    "White has captured {} pieces.".format(captured[Player.WHITE]),
    "",
    "It is {}'s turn.".format(player.value)
  ]
  output = ""
  for b, h in zip_longest(drawing.split('\n'), HELP_TEXT.split('\n') + status, fillvalue=""):
    output += "{}  {}\n".format(b, h)
  print(output)

# ---- Constants/Predefined --------------------------------

BOARD_BOUNDARY = 18
"""The board boundary, for which indexing with a larger value results in an
error."""

BLACK_PIECES = 48
"""The amount of black pieces initially on the board."""
WHITE_PIECES = 25
"""The amount of white pieces initially on the board."""

INITIAL_BOARD = [
  [Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.WOLF,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.WOLF],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.KING,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.WOLF,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.WOLF],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.PAWN,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF],
  [Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE],
  [Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE,Piece.WOLF,Piece.NONE,Piece.NONE],
]
"""The initial board setup."""

MARKED_POSITIONS = {
  (0,0),
  (0,1),
  (1,0),
  (1,1),
  (0,17),
  (0,18),
  (1,17),
  (1,18),
  (17,0),
  (18,0),
  (17,1),
  (18,1),
  (17,17),
  (17,18),
  (18,17),
  (18,18),
  (9,9),
}
"""A set of the marked positions of the board."""

MIDDLE_POSITION = (9,9)
"""The middle marked position of the board."""

HELP_TEXT = ("\
Alea Evangelii\n\
\n\
Pieces move either horizontally or\n\
vertically, for as many steps as wanted.\n\
However, a piece may not jump over\n\
another, and may not land in a non-empty\n\
square. The king moves in the same manner,\n\
but is limited to a maximum of four steps.\n\
\n\
Pieces are captured by surrounding an\n\
opponent piece either horizontally or\n\
vertically with two of one's own pieces.\n\
Captured pieces are removed from the board.\n\
\n\
The king requires three non-diagonally\n\
adjacent opponent pieces to be captured.\n\
\n\
Squares marked with a ⌃ symbol count as a\n\
piece for either player for captures.\n\
\n\
The game is won if: either black captures\n\
the king; or white moves the king to one\n\
of the marked corner squares.\n\
")
"""Help text printed alongside the board."""

if __name__ == "__main__":
  startParams = (Mode.HUMANB_VS_AIW, Player.WHITE, Player.BLACK)
  playGame(startParams)
