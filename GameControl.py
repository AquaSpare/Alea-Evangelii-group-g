#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 13:33:52 2021

@author: leeyu-sun
"""
from GameEngine import GameState, Move
from gameAI import findBestMove, findRandomMove

class player(object):
    def __init__(self,ai,position,difficulty):
        self.ai = ai
        self.position = position # 'w':white 1'b':black
        self.difficulty = difficulty # 0: easy , 1: hard
    def isAi(self):
        self.ai = True
    

class GameControl():
    def __init__(self):
        self.playerNow = 0
        self.numTurns = 0
    # how many true players
    def setPlayer(self,num,playerList):
        choose = [[True,True],[False,True],[True,False],[False,False]]
        if num == '1' :
            whiteOrBlack = input('Select which side white or black: ') #input 0:white 1:black
            playerList[0].ai,playerList[1].ai = choose[1+int(whiteOrBlack)]
        if num == '2' :
            playerList[0].ai,playerList[1].ai = choose[3]
        if num == '0':
            playerList[0].ai,playerList[1].ai = choose[0]
    
    # set up difficulty 0:random 1:minmax
    def setDifficulty(self,playerList):
        for player in playerList:
            if player.ai == True:
                player.difficulty = input('Select ai difficulty 0: easy , 1: hard : ')
    
    #change player
    def switchPlayer(self,gs):
        self.playerNow = self.playerNow * -1 + 1
        self.numTurns += 1
    #There is same funtion in the gamestate.implement here?? equal win
    def endgame(gs):
        pass
    
    #Well perform in the gamestate . modify it if we want play()funtion looks more concise
    def legalMove(self,gs,p):
        pass
    
    #one player's turn.
    def play(self,gs,p):
        #Ai turn
        if p.ai == True :
            possibleMoves = gs.getAllPossibleMoves()
            AIMove = findBestMove(gs,possibleMoves)
            print(AIMove)
            gs.makeMove(AIMove)
            return True
        # human turn    
        else :
            possibleMoves = gs.getAllPossibleMoves()
            sq1 = input('Select square to move from: ') #input square you want to move from int,int
            sq2 = input('Select square to move to: ') #input square you want to move to int,int

            startSq = tuple(int(x) for x in sq1.split(","))
            endSq = tuple(int(x) for x in sq2.split(","))
            if startSq != endSq:
                move = Move(startSq,endSq,gs.board)
                if move in possibleMoves:
                    gs.makeMove(move)
                    prompt = input("undo??")

                    if prompt == 'undo':
                        print('undoing')
                        gs.undoMove()
                        return  False
                    return True

            if startSq == endSq:
                print('Try again')
                return False
    #display game information        
    def gameInfo(self,p):
        print("-----Turns number %d , %s turns----"%(int(self.numTurns/2)+1,p.position))
        
            
def drawBoard(board):
    # Function that prints out the current boardstate
    for row in board:
        print('{}'.format(row))           
            
            
        
def main():
    # Create an object of the class GameState and Gamecontrol
    gs = GameState()
    gc = GameControl()
    #Create player and put into list
    p1 = player(True,"White",1)
    p2 = player(False,"Black",1)
    playerList = []
    playerList.append(p1)
    playerList.append(p2)
    #set up the number of the player 
    number = input('How many real players : ')
    gc.setPlayer(number,playerList)
    gc.setDifficulty(playerList)
    # A list of all possible moves on the board
    #running = True
    #moveMade = False

    
    # Loop for every turn, switches between any two players
    while gs.win == False:
        drawBoard(gs.board)
        p = playerList[gc.playerNow]
        gc.gameInfo(p)
        if gc.play(gs,p) == True:
            gc.switchPlayer(gs)
        input("draw Board")
        drawBoard(gs.board)
        print('\n-------------------------------------------------------------------------------------------------------------\n')

if __name__ == "__main__":
    main()

        

        
        
        
        
        
