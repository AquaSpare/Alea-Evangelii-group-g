from AImove import computerMove
from GameEngine import GameState
from gameMain import drawBoard

turn = 0;
gs = GameState()
drawBoard(gs.board)

turn = computerMove(gs,'hard',turn)
drawBoard(gs.board)