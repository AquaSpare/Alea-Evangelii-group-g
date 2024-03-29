class GameState():
    # constructor of GameState object
    def __init__(self):
        # Board is a 19*19 2D list each elemet has 2 characters.
        # The first character represent color "b" or "w".
        # The second character represent the type of pice "K" or "p".

        # This board is set to the initial board, and has been used in testing. Kept as a reference on how we store the
        # board.

        self.board = [
            ["--", "--", "bp", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "bp", "--",
             "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--",
             "--"],
            ["bp", "--", "--", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "--", "--",
             "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "bp", "--", "bp", "--", "bp", "--", "--", "--", "--", "--", "--",
             "--"],
            ["--", "--", "--", "bp", "--", "--", "bp", "--", "wp", "--", "wp", "--", "bp", "--", "--", "--", "--", "--",
             "--"],
            ["bp", "--", "bp", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "bp", "--",
             "bp"],
            ["--", "--", "--", "--", "bp", "--", "--", "--", "--", "wp", "--", "--", "--", "--", "bp", "--", "--", "--",
             "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--", "wp", "--", "wp", "--", "--", "--", "--", "bp", "--", "--",
             "--"],
            ["--", "--", "--", "--", "wp", "--", "--", "wp", "--", "wp", "--", "wp", "--", "--", "wp", "--", "--", "--",
             "--"],
            ["--", "--", "--", "bp", "--", "--", "wp", "--", "wp", "wK", "wp", "--", "wp", "--", "--", "bp", "--", "--",
             "--"],
            ["--", "--", "--", "--", "wp", "--", "--", "wp", "--", "wp", "--", "wp", "--", "--", "wp", "--", "--", "--",
             "--"],
            ["--", "--", "--", "bp", "--", "--", "--", "--", "wp", "--", "wp", "--", "--", "--", "--", "bp", "--", "--",
             "--"],
            ["--", "--", "--", "--", "bp", "--", "--", "--", "--", "wp", "--", "--", "--", "--", "bp", "--", "--", "--",
             "--"],
            ["bp", "--", "bp", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "bp", "--",
             "bp"],
            ["--", "--", "--", "--", "--", "--", "bp", "--", "wp", "--", "wp", "--", "bp", "--", "--", "--", "--", "--",
             "--"],
            ["--", "--", "--", "--", "--", "--", "--", "bp", "--", "bp", "--", "bp", "--", "--", "--", "--", "--", "--",
             "--"],
            ["bp", "--", "--", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "--", "--",
             "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--",
             "--"],
            ["--", "--", "bp", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "bp", "--",
             "--"],
        ]

        # Properties of the GameState
        self.moveFunctions = {'p': self.getPawnMoves, 'K': self.getKingMoves}
        self.movelog = []
        self.whiteToMove = True
        self.win = False

    # Moves a piece, records the movement in the movelog, upadates turn order, and checks if the player wins.
    def makeMove(self, move):
        corners = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 17), (0, 18), (1, 17), (1, 18), (17, 0), (17, 1), (18, 0),
                   (18, 1), (17, 17), (17, 18), (18, 17), (18, 18)]  # does not include middle square

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)  # log the move
        self.whiteToMove = not self.whiteToMove  # switch player to move

        self.updateCapture(move.endRow, move.endCol, move)

        # check if king has moved to winning position
        if (move.pieceMoved[1] == 'K') and ((move.endRow, move.endCol) in corners):
            self.win = True

    # Checks if a given piece can capture if it is moved to a place on the board. If the conditions to capture a pawn
    # is fulfilled the pawn that is captured is added to pieceCaptured_cord and removed from the board. If the
    # conditions to capture the king is fulfilled the king is removed and the black player wins.
    def updateCapture(self, row, col, move):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # directions up, left, down, right
        corners = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 17), (0, 18), (1, 17), (1, 18), (17, 0), (17, 1), (18, 0),
                   (18, 1), (17, 17), (17, 18), (18, 17), (18, 18), (9, 9)]

        # possible combinations of pawn capture neighbourhood
        cap1 = ['b', 'w', 'b']
        cap2 = ['w', 'b', 'w']
        cap3 = ['w', 'b', 'corner']
        cap4 = ['b', 'w', 'corner']
        cap = [cap1, cap2, cap3, cap4]

        # possible combinations of King capture neighbourhood
        cap1_K = ['b', 'b', 'b']
        cap2_K = ['corner', 'b', 'b']
        cap3_K = ['b', 'corner', 'b']
        cap4_K = ['b', 'b', 'corner']
        cap5_K = ['corner', 'corner', 'b']
        cap6_K = ['corner', 'b', 'corner']
        cap7_K = ['b', 'corner', 'corner']
        cap_K = [cap1_K, cap2_K, cap3_K, cap4_K, cap5_K, cap6_K, cap7_K]

        for d in directions:
            sequence = []
            neigbourhoodKing = []
            sequence.append(self.board[row][col][0])
            for i in range(1, 3):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 19 and 0 <= endCol < 19:  # see if it still inside the grid
                    endPiece = self.board[endRow][endCol]
                    if (endPiece == '--') and (
                            i == 1):  # does not capture in this direction if first neighbour is blank
                        break

                    elif (endPiece[1] == 'K') and (i == 1):  # if closest neighbour is king
                        for d_K in directions:
                            endRow_K = endRow + d_K[0]
                            endCol_K = endCol + d_K[1]
                            if 0 <= endRow_K < 19 and 0 <= endCol_K < 19:  # see if it still inside the grid
                                endPiece_K = self.board[endRow_K][endCol_K]
                                if endPiece_K[0] == 'b':
                                    neigbourhoodKing.append('b')
                                elif (endRow_K, endCol_K) in corners:
                                    neigbourhoodKing.append('corner')
                    elif (i == 2) and ((endRow, endCol) in corners):
                        sequence.append('corner')
                    else:
                        sequence.append(endPiece[0])

                else:  # we have gone off the board
                    break

            if sequence in cap:  # a pawn is captured
                move.pieceCaptured = self.board[row + d[0]][col + d[1]]
                move.pieceCaptured_cord = (row + d[0], col + d[1])

                self.board[row + d[0]][col + d[1]] = '--'

            elif neigbourhoodKing in cap_K:  # king is captured
                move.pieceCaptured = self.board[row + d[0]][col + d[1]]
                move.pieceCaptured_cord = (row + d[0], col + d[1])

                self.board[row + d[0]][col + d[1]] = '--'
                self.win = True

    # Reverse the last move in the move log
    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = '--'
            self.whiteToMove = not self.whiteToMove

            if move.pieceCaptured:
                self.board[move.pieceCaptured_cord[0]][move.pieceCaptured_cord[1]] = move.pieceCaptured

            self.win = False

    # Gets all possible moves for all pieces on a given board and returns them in a list "moves"
    def getAllPossibleMoves(self):
        moves = []

        if self.win:
            return moves

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if ((turn == 'w') and self.whiteToMove) or ((turn == 'b') and (not self.whiteToMove)):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row, col, moves)
        return moves

    # Adds all valid moves of a given pawn to the list "moves"
    def getPawnMoves(self, row, col, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # directions up, left, down, right
        for d in directions:
            for i in range(1, 19):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 19 and 0 <= endCol < 19:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    else:  # piece in the way, invalid
                        break
                else:  # we have gone off the board
                    break

    # Adds all valid moves of a given king to the list "moves"
    def getKingMoves(self, row, col, moves):
        directions = (
            (-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1))  # directions up, left, down, right
        # and diagonals
        for d in directions:
            for i in range(1, 5):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 19 and 0 <= endCol < 19:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row, col), (endRow, endCol), self.board))
                    else:  # piece in the way, invalid
                        break
                else:  # we have gone off the board
                    break


# Class used to define a move
class Move():

    filesToRows = {"S":18,"R":17,"Q":16,"P":15,"O":14,"N":13,"M":12,"L":11,"K":10,"J":9,"I":8,"H":7,"G":6,"F":5,"E":4,"D":3,"C":2,"B":1,"A":0}
    rowsToFiles = {v: k for k,v in filesToRows.items()}

    rankToCols = {"1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"10":9,"11":10,"12":11,"13":12,"14":13,"15":14,"16":15,"17":16,"18":17,"19":18}
    colsToRank = {v: k for k,v in rankToCols.items()}


    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow *10 + self.endCol

        self.pieceCaptured = False
        self.pieceCaptured_cord = None

    def __str__(self):
        return '({}) -> ({})'.format(self.getNotation()[0],self.getNotation()[1])

    def __eq__(self, other):  # override equals method
        if isinstance(other, Move):
            return self.moveID == other.moveID

        # need to find what pice is being captured for a moce
        # self.piceCaptured =

    def getNotation(self):
        return (self.getRankFile(self.startRow,self.startCol),self.getRankFile(self.endRow,self.endCol))

    def getRankFile(self,r,c):
        return self.rowsToFiles[r] + self.colsToRank[c]