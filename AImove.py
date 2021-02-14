
from gameAI import findBestMove, findRandomMove


def computerMove(gs,difficulty,turn):

    print(difficulty)

    possibleMoves = gs.getAllPossibleMoves()
    if (difficulty == 'easy'):
        AImove = findRandomMove(possibleMoves)
    elif (difficulty == 'hard'):
        AImove = findBestMove(gs,possibleMoves)
    else:
        print('{} is not a valid difficulty'.format(difficulty))
        return turn

    print(AImove)
    gs.makeMove(AImove)

    return turn+1
