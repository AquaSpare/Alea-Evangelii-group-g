# The AI, can choose between getting a randome move or the "best" move
import random

# Give a bias to the king
pieceScore = {'K':100,'p':5}
GAMEOVER = 1000

# Returns one of the possible moves, chosen at randome
def findRandomMove(possibleMoves):
    return possibleMoves[random.randint(0,len(possibleMoves)-1)]

# Returns one of the possible moves, chooses the move with highest score
# Looks though every move and give them a score, keep the move with the highest score

def findBestMove(gs,possibleMoves):
    turnMultiplyer = 1 if gs.whiteToMove else -1

    maxScore = -GAMEOVER
    bestMove = None
    for playerMove in possibleMoves:
        gs.makeMove(playerMove)
        score = scoreMaterial(gs.board)
        if gs.win:
            score = GAMEOVER
        else:
            score = turnMultiplyer * scoreMaterial(gs.board) # MAYBE WE CAN USE "score" HERE? SHOULD BE THE SAME WE CALCULATED ABOVE?
        if (score > maxScore):
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove


# Score the board
# The score is higher if there are many of your own pieces, and less of the enemies pieces
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'b':
                score -= pieceScore[square[1]]
            if square[0] == 'w':
                score += pieceScore[square[1]]
    return score
