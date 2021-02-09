import random

pieceScore = {'K':100,'p':5}
GAMEOVER = 1000

def findRandomMove(possibleMoves):
    return possibleMoves[random.randint(0,len(possibleMoves)-1)]


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
            score = turnMultiplyer * scoreMaterial(gs.board)
        if (score > maxScore):
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove



#score the board
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'b':
                score -= pieceScore[square[1]]
            if square[0] == 'w':
                score += pieceScore[square[1]]
    return score