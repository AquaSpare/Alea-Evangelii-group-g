# The AI, can choose between getting a random move or the "best" move
import random

# Give a bias to the king
pieceScore = {'K': 100, 'p': 5}
GAMEOVER = 1000
DEPTH = 2


# Returns one of the possible moves, chosen at random
def findRandomMove(possibleMoves):
    return possibleMoves[random.randint(0, len(possibleMoves) - 1)]


# Returns one of the possible moves, chooses the move with highest score
# Looks though every move and give them a score, keep the move with the highest score
def findBestMove(gs, possibleMoves):
    turnMultiplyer = 1 if gs.whiteToMove else -1

    maxScore = -GAMEOVER
    bestMove = None
    for playerMove in possibleMoves:
        gs.makeMove(playerMove)
        score = scoreMaterial(gs.board)
        if gs.win:
            score = GAMEOVER
        else:
            score = turnMultiplyer * scoreMaterial(
                gs.board)  # MAYBE WE CAN USE "score" HERE? SHOULD BE THE SAME WE CALCULATED ABOVE?
        if (score > maxScore):
            maxScore = score
            bestMove = playerMove
        gs.undoMove()
    return bestMove


# helper method to make the first recursive call, to change global variable DEPTH determine how many moves ahead is
# considered
def findBestMoveMinMax(gs, possibleMoves):
    global nextMove
    nextMove = None
    random.shuffle(possibleMoves)
    # findMoveNegaMax(gs, possibleMoves, DEPTH, 1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, possibleMoves, DEPTH, -GAMEOVER, GAMEOVER, 1 if gs.whiteToMove else -1)

    if nextMove is None:
        return findRandomMove(possibleMoves)
    else:
        return nextMove


# implementation of minmax algorithm
def findMoveMinMax(gs, possibleMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -GAMEOVER
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossibleMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            print(score)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = GAMEOVER
        for move in possibleMoves:
            gs.makeMove(move)
            nextMoves = gs.getAllPossibleMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


# implementation of minmax algorithm with nega max structure
def findMoveNegaMax(gs, possibleMoves, depth, turnMultiplyer):
    global nextMove
    if depth == 0:
        return turnMultiplyer * scoreBoard(gs)

    maxScore = -GAMEOVER
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossibleMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplyer)
        if score > maxScore:
            maxScore = score
            # print("depth: {} move: {} score {}, nextMove: {}".format(depth,move,score,nextMove))
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


# implementation of alpha beta pruning in combination with nega max
def findMoveNegaMaxAlphaBeta(gs, possibleMoves, depth, alpha, beta, turnMultiplyer):
    global nextMove
    if depth == 0:
        return turnMultiplyer * scoreBoard(gs)

    # move ordering - implement later
    maxScore = -GAMEOVER
    for move in possibleMoves:
        gs.makeMove(move)
        nextMoves = gs.getAllPossibleMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplyer)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # pruning happend
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


# a positive score is good for white, a negative score is good for black
def scoreBoard(gs):
    if gs.win:
        if gs.whiteToMove:
            return -GAMEOVER  # black wins
        else:
            return GAMEOVER

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'b':
                score -= pieceScore[square[1]]
            if square[0] == 'w':
                score += pieceScore[square[1]]
    return score


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
