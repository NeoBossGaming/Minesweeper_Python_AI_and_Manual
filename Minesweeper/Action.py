class GameAction:
    def __init__(self, board):
        self.board = board
        self.flaggedLocations = []
    def flagLocation(self, locationX, locationY):
        self.board.updateBoard(locationX, locationY, "F")
        self.flaggedLocations.append((locationX, locationY))
    def revealLocation(self, locationX, locationY):
        self.board.updateBoard(locationX, locationY, self.board.completeBoard[locationX][locationY])
    def unflagLocation(self, locationX, locationY):
        self.board.updateBoard(locationX, locationY, "?")
        if (locationX, locationY) in self.flaggedLocations:
            self.flaggedLocations.remove((locationX, locationY))
        else:
            return "User Error, location given is not yet flagged"
    def exit(self):
        pass