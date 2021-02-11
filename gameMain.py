# This is a test file to test that the Eninge works properly. It lets a human play against the engine.
# Run this file to test the engine. After inputing a move press Enter untill board gets printed again.
# Not part of end product
from GameEngine import GameState, Move
from gameAI import findBestMove, findRandomMove


# Print the board to help visualise
def drawBoard(board):
    # Function that prints out the current boardstate
    for row in board:
        print('{}'.format(row))

# Main to test that everything works, includes a way for a human to play against the  AI
def main():
    # Create an object of the class GameState
    gs = GameState()
    # A list of all possible moves on the board
    possibleMoves = gs.getAllPossibleMoves()
    running = True
    moveMade = False

    playerOne = True #if a human is playing True, if AI playing false
    playerTwo = False # if a human is playing True, if AI playing false
    
    # Loop for every turn, switches between a human and the AI
    while running and (not gs.win):
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        drawBoard(gs.board)
        
        
        # Asks for a human player to make a move
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
