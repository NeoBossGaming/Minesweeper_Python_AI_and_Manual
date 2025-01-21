from Board import GameBoard
from Action import GameAction

class GameController:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 1: # Easy difficulty
            self.playBoard = GameBoard(10, 10, 0.2)
        
        if difficulty == 2: # Medium difficulty
            self.playBoard = GameBoard(20, 20, 0.3)

        if difficulty == 3: # Hard difficulty
            self.playBoard = GameBoard(50, 50, 0.4)

        self.playBoard.setupBoard()
        self.actionManager = GameAction(self.playBoard)

    def showBoard(self):
        return self.playBoard.returnPlayBoard()
    
    def executeAction(self, action, xLoc, yLoc):
        validActions = [1, 2, 3, 4]
        if action not in validActions: # Validate if executable action
            return "Action unvalid, must be either [1(Reveal), 2(Flag), 3(Unflag), 4(Cancel)]"
        
        if action == 1: # Reveal
            self.actionManager.revealLocation(yLoc, xLoc)
            print("Done Revealing")
        if action == 2: # Flag
            self.actionManager.flagLocation(yLoc, xLoc)
        
        if action == 3: # Unflag
            self.actionManager.unflagLocation(yLoc, xLoc)

        if action == 4: # Leave
            pass

    def checkIfWin(self):
        for i in self.playBoard.playBoard:
            if "?" in i:
                return False
            else:
                continue
        return True