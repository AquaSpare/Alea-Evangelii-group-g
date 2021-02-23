
class GameState():
    #constructor of GameState object if no parameters as given input
    def __init__(self):
        # Board is a 19*19 2D list each elemet has 2 characters.
        # The first character represent color "b" or "w".
        # The second character represent the type of pice "K" or "p".
        
        # This board is to test that everything works
        # Not part of end product
        self.board = [
            ["bp","wp","bp","--","--","bp","--","--","--","--","--","--","--","bp","--","--","bp","--","--"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["wK","bp","--","--","--","bp","--","--","--","--","--","--","--","bp","--","--","--","--","bp"],
            ["bp","wp","--","--","--","--","--","bp","--","bp","--","bp","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","bp","--","wp","--","wp","--","bp","--","--","--","--","--","--"],
            ["bp","--","bp","--","--","bp","--","--","--","--","--","--","--","bp","--","--","bp","--","bp"],
            ["--","--","--","--","bp","--","--","--","--","wp","--","--","--","--","bp","--","--","--","--"],
            ["--","--","--","bp","--","--","--","--","wp","--","wp","--","--","--","--","bp","--","--","--"],
            ["--","--","--","--","wp","--","--","wp","--","--","--","wp","--","--","wp","--","--","--","--"],
            ["--","--","--","bp","--","--","wp","--","wp","--","wp","--","wp","--","--","bp","--","--","--"],
            ["--","--","--","--","wp","--","--","wp","--","wp","--","wp","--","--","wp","--","--","--","--"],
            ["--","--","--","bp","--","--","--","--","wp","--","wp","--","--","--","--","bp","--","--","--"],
            ["--","--","--","--","bp","--","--","--","--","wp","--","--","--","--","bp","--","--","--","--"],
            ["bp","--","bp","--","--","bp","--","--","--","--","--","--","--","bp","--","--","bp","--","bp"],
            ["--","--","--","--","--","--","bp","--","wp","--","wp","--","bp","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","bp","--","bp","--","bp","--","--","--","--","--","--","--"],
            ["bp","--","--","--","--","bp","--","--","--","--","--","--","--","bp","--","--","--","--","bp"],
            ["--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--","--"],
            ["--","--","bp","--","--","bp","--","--","--","--","--","--","--","bp","--","--","bp","--","--"],
        ]
        
        # Properties of the board
        self.moveFunctions = {'p': self.getPawnMoves, 'K': self.getKingMoves}
        self.movelog = []
        self.whiteToMove = True
        self.win = False

        
    # Moves a piece, records the movement in the movelog, upadates turn order, and checks if the player wins.
    def makeMove(self,move):
        # Takes a move object as input and excecutes it on the baord of the gamestate
        corners = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 17), (0, 18), (1, 17), (1, 18), (17, 0), (17, 1), (18, 0),
                   (18, 1), (17, 17), (17, 18), (18, 17), (18, 18)] # does not include middle square

        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move) #log the move
        self.whiteToMove = not self.whiteToMove #switch player to move

        self.updateCapture(move.endRow,move.endCol,move)

        #check if king has moved to winning position
        if (move.pieceMoved[1] == 'K') and ((move.endRow,move.endCol) in corners):
            self.win = True

    # Checks if a given piece can capture if it is moved to a place on the board. 
    # If the conditions to caputre a pawn is fulfilled the pawn that is captured is added to pieceCaptured_cord and removed from the board.
    # If the conditions to capture the king is fullfilled the king is removed and the black player wins.
    def updateCapture(self,row,col,move):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # directions up, left, down, right
        corners = [(0,0),(0,1),(1,0),(1,1),(0,17),(0,18),(1,17),(1,18),(17,0),(17,1),(18,0),(18,1),(17,17),(17,18),(18,17),(18,18),(9,9)] #inlcudes middle square

        #possible combinations of pawn capture neigbourhood
        cap1 = ['b','w','b']
        cap2 = ['w','b','w']
        cap3 = ['w','b','corner']
        cap4 = ['b','w','corner']
        cap = [cap1,cap2,cap3,cap4]

        #possible combinations of King capture neighbourhood
        cap1_K = ['b','b','b']
        cap2_K = ['corner','b','b']
        cap3_K = ['b','corner','b']
        cap4_K = ['b','b','corner']
        cap5_K = ['corner','corner','b']
        cap6_K = ['corner','b','corner']
        cap7_K = ['b','corner','corner']
        cap_K = [cap1_K,cap2_K,cap3_K,cap4_K,cap5_K,cap6_K,cap7_K]

        for d in directions:
            sequence = []
            neigbourhoodKing = []
            sequence.append(self.board[row][col][0])
            for i in range(1, 3):
                endRow = row + d[0] * i
                endCol = col + d[1] * i
                if 0 <= endRow < 19 and 0 <= endCol < 19: #see if it still inside the grid
                    endPiece = self.board[endRow][endCol]
                    if (endPiece == '--') and (i == 1): #does not capture in this direction if first neighbour is blank
                        break

                    elif (endPiece[1] == 'K') and (i == 1): #if closest neighbour is king
                        for d_K in directions:
                            endRow_K = endRow + d_K[0]
                            endCol_K = endCol + d_K[1]
                            if 0 <= endRow_K < 19 and 0 <= endCol_K < 19:  # see if it still inside the grid
                                endPiece_K = self.board[endRow_K][endCol_K]
                                if endPiece_K[0] == 'b':
                                    neigbourhoodKing.append('b')
                                elif (endRow_K,endCol_K) in corners:
                                    neigbourhoodKing.append('corner')
                    elif (i == 2) and ((endRow,endCol) in corners):
                        sequence.append('corner')
                    else:
                        sequence.append(endPiece[0])

                else:  # we have gone off the board
                    break

            print(neigbourhoodKing)

            if sequence in cap: #a pawn is captured
                move.pieceCaptured = self.board[row+d[0]][col+d[1]]
                move.pieceCaptured_cord = (row+d[0],col+d[1])

                self.board[row+d[0]][col+d[1]] = '--'


            elif neigbourhoodKing in cap_K : #king is captured
                self.board[row+d[0]][col+d[1]] = '--'
                self.win = True


    # Reverse the last move in the movelog
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
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (((turn == 'w') and self.whiteToMove) or ((turn == 'b') and (not self.whiteToMove))):
                    piece = self.board[row][col][1]
                    self.moveFunctions[piece](row,col,moves)  # ARE YOU SURE THIS WORKS AS INTENDED? For me "(row,col,moves)" is marked as unexpected arguments

        if len(moves) == 0:
            self.gameOver = True
        return moves

    # Adds all valid moves of a given pawn to the list "moves"
    def getPawnMoves(self,row,col,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) # directions up, left, down, right
        for d in directions:
            for i in range(1,19):
                endRow = row + d[0]*i
                endCol = col + d[1]*i
                if 0 <= endRow < 19 and 0 <= endCol < 19:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':
                        moves.append(Move((row,col),(endRow,endCol),self.board))
                    else: #piece in the way, invalid
                        break
                else: # we have gone off the board
                    break

    # Adds all valid moves of a given king to the list "moves"
    def getKingMoves(self,row,col,moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1),(1,1),(1,-1),(-1,1),(-1,-1))  # directions up, left, down, right
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


# Class used to define movment
class Move():
    def __init__(self,startSq,endSq,board):

        self.startRow = startSq[0]
        self.startCol = startSq[1]

        self.endRow = endSq[0]
        self.endCol = endSq[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow + self.endCol

        self.pieceCaptured = False
        self.pieceCaptured_cord = None

    def __str__(self):
        return '({},{}) -> ({},{})'.format(self.startRow,self.startCol,self.endRow,self.endCol)



    def __eq__(self, other): #override equals method
        if isinstance(other,Move):
            return self.moveID == other.moveID

        # need to find what pice is being captured for a moce
        # self.piceCaptured =
