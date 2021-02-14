from gameAI import findBestMove, findRandomMove


#function that takes a gamestate and excecute the move on the board of the gamestate, given a difficulty.
#Inputs: gs (game state object), difficulty ('easy' or 'hard'), turn (integer turn counter)
#Output: updated turn counter if move is made.

def computerMove(gs,difficulty,turn):

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
