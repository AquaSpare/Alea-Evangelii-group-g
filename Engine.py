import random
from GameEngine import GameState, Move
from gameAI import findBestMove, findRandomMove
from gameMain import drawBoard

# This is the function that will be called in other components.
# It lets the AI play one turn.
# If it is one of the first two turns it asks for a difficulty that is used for the rest of the game
def engine(board, turn):
    # choose the difficulty
    global diff0
    global diff1
    if turn == 0:
        diff0 = int(input('Select ai difficulty 0: easy , 1: hard : '))
    elif turn == 1:
        diff1 = int(input('Select ai difficulty 0: easy , 1: hard : '))
    if turn % 2 == 0:
        diff = diff0
    else:
        diff = diff1

    gs = GameState()
    gs.board = boardtrasnlation(board)
    if diff == 0:  # for easy AI
        # The chance of picking a random move should be tweaked
        if random.random() < 0.85:  # 15% chance to pick a random move85% chance to pick the best move
            possibleMoves = gs.getAllPossibleMoves()
            AIMove = findBestMove(gs, possibleMoves)
            gs.makeMove(AIMove)
            return gs.board, (turn + 1)
        else:  # 15% chance to pick a random move
            possibleMoves = gs.getAllPossibleMoves()
            AIMove = findRandomMove(possibleMoves)
            gs.makeMove(AIMove)
            return gs.board, (turn + 1)
    elif diff == 1:  # for hard AI
        possibleMoves = gs.getAllPossibleMoves()
        AIMove = findBestMove(gs, possibleMoves)
        gs.makeMove(AIMove)
        return gs.board, (turn + 1)
    else:
        raise Exception("Error, difficulty chosen is not 0 or 1.")


# Translate the board to our board, has to be written when we know what the inputboard looks like
def boardtrasnlation(board):
    return board


# TO TEST engine
def main():
    board = [
        ["--", "--", "bp", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "bp", "--",
         "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--",
         "--"],
        ["bp", "--", "--", "--", "--", "bp", "--", "--", "--", "--", "--", "--", "--", "bp", "--", "--", "--", "--",
         "bp"],
        ["--", "--", "--", "--", "--", "--", "--", "bp", "--", "bp", "--", "bp", "--", "--", "--", "--", "--", "--",
         "--"],
        ["--", "--", "--", "--", "--", "--", "bp", "--", "wp", "--", "wp", "--", "bp", "--", "--", "--", "--", "--",
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
    turn = 0
    end = 0
    gs = GameState
    gs.board = board
    while turn < 100:
        [gs.board, turn] = engine(gs.board, turn)
        print(turn)
        drawBoard(gs.board)


if __name__ == "__main__":
    main()
