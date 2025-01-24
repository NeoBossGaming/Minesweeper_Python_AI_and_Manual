from Board import GameBoard
from Action import GameAction


class GameController:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        if difficulty == 1:  # Easy difficulty
            self.playBoard = GameBoard(8, 8, 0.125)

        if difficulty == 2:  # Medium difficulty
            self.playBoard = GameBoard(16, 16, 0.16)

        if difficulty == 3:  # Hard difficulty
            self.playBoard = GameBoard(20, 20, 0.25)

        self.playBoard.setupBoard()
        self.actionManager = GameAction(self.playBoard)

    def showBoard(self):
        return self.playBoard.returnPlayBoard()

    def executeAction(self, action, xLoc, yLoc):
        validActions = [1, 2, 3, 4]
        if action not in validActions:  # Validate if executable action
            return "Action unvalid, must be either [1(Reveal), 2(Flag), 3(Unflag), 4(Cancel)]"

        if action == 1:  # Reveal
            self.actionManager.revealLocation(xLoc, yLoc)
            return self.showBoard()[yLoc][xLoc]

        if action == 2:  # Flag
            self.actionManager.flagLocation(xLoc, yLoc)
        if action == 3:  # Unflag
            self.actionManager.unflagLocation(xLoc, yLoc)
        if action == 4:  # Leave
            return "End"

    def checkIfWin(self):
        for i in self.playBoard.returnPlayBoard():
            if "?" in i:
                return False
            else:
                continue
        return True