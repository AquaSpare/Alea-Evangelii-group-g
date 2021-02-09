from GameEngine import GameState, Move
from gameAI import findBestMove, findRandomMove



def drawBoard(board):
    # Function that prints out the current boardstate
    for row in board:
        print('{}'.format(row))


def main():

    gs = GameState()
    possibleMoves = gs.getAllPossibleMoves()
    running = True
    moveMade = False

    playerOne = True #if a human is playing True, if AI playing false
    playerTwo = False # if a human is playing True, if AI playing false

    while running and (not gs.win):
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        drawBoard(gs.board)

        if humanTurn:

            sq1 = input('Select square to move from: ') #input square you want to move from int,int
            sq2 = input('Select square to move to: ') #input square you want to move to int,int

            startSq = tuple(int(x) for x in sq1.split(","))
            endSq = tuple(int(x) for x in sq2.split(","))

            if startSq != endSq:
                move = Move(startSq,endSq,gs.board)
                if move in possibleMoves:
                    gs.makeMove(move)
                    moveMade = True

            if startSq == endSq:
                print('Try again')

            prompt = input()

            if prompt == 'undo':
                print('undoing')
                gs.undoMove()
                moveMade = False

        #AI move finder
        if not humanTurn:
            AIMove = findBestMove(gs,possibleMoves)
            print(AIMove)

            gs.makeMove(AIMove)
            moveMade = True

        if moveMade:
                possibleMoves = gs.getAllPossibleMoves()
                moveMade = False

                if gs.win:
                    print('End of game')

        input()
        drawBoard(gs.board)
        print('\n-------------------------------------------------------------------------------------------------------------\n')

if __name__ == "__main__":
    main()
