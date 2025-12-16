import random


class GameBoard:
    def __init__(self, xDimen, yDimen, minePer):
        self.xDimen = xDimen  # Width of the board
        self.yDimen = yDimen  # Height of the board
        self.minePer = minePer  # Percentage of mines
        self.mineLocation = None
        self.completeBoard = None
        self.playBoard = None

    def setupBoard(self):
        self.createBoard()
        self.insertMineToBoard()
        self.insertNumbersToBoard()
        self.createBlurryBoard()
        return self.returnPlayBoard()

    def createBoard(self):  # Make the empty board, filled with 0
        verticalBoardLength = self.yDimen  # Amount of cells located on the vertical axis
        horizontalBoardLength = self.xDimen  # Amount of cells located on the horizontal axis

        mineLocations = []  # Initialize variable for mines

        for y in range(verticalBoardLength):  # Initializing 2D Array
            mineLocations.append([])

            for x in range(horizontalBoardLength):  # Add 0 in each row
                mineLocations[y].append("0")
        self.mineLocation = mineLocations
        return mineLocations

    def insertMineToBoard(self):
        if self.mineLocation is None:
            return "Error Message: Has not initialize self.mineLocation, Try calling createBoard()"

        cellsInBoard = self.xDimen * self.yDimen  # Find total tiles in board
        mineAmount = int(round((cellsInBoard * self.minePer), 0))
        for i in range(mineAmount):
            luckyX = random.randint(0, self.xDimen - 1)  # x location that will be turned into a mine
            luckyY = random.randint(0, self.yDimen - 1)  # y location that will be turned into a mine

            while self.mineLocation[luckyY][luckyX] == "9":  # reroll luckyX and luckyY
                luckyX = random.randint(0, self.xDimen - 1)
                luckyY = random.randint(0, self.yDimen - 1)

            self.mineLocation[luckyY][luckyX] = "9"
        return self.mineLocation

    def insertNumbersToBoard(self):
        if self.mineLocation == None:
            return "Error Message: Has not initialize self.mineLocation, Try calling createBoard()"

        self.completeBoard = list()  # Create template list containing numbers
        for y in range(self.yDimen):  # Initialize 2D Board
            self.completeBoard.append([])  # Create a line in this row
            for _ in range(self.xDimen):
                self.completeBoard[y].append("0")
        for x in range(self.yDimen):  # Loop through vertical row
            for y in range(self.xDimen):  # Loop through each tile in row
                if self.mineLocation[x][y] == str("9"):
                    self.completeBoard[x][y] = "9"  # Put mine in the template board
                    surrCoords = [  # List of all the surrounding tiles of non mines
                        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
                        (x - 1, y), (x + 1, y),
                        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
                    ]

                    for coor in surrCoords:  # In each
                        if 0 <= coor[0] < self.yDimen and 0 <= coor[1] < self.xDimen:
                            if self.completeBoard[coor[0]][coor[1]] != "9":  # Don't update if it's a mine
                                self.completeBoard[coor[0]][coor[1]] = str(
                                    int(self.completeBoard[coor[0]][coor[1]]) + 1)
        return self.completeBoard

    def createBlurryBoard(self):
        if self.completeBoard == None:  # Check if template list or complete list has already been made or not
            return " Error Message: Has not initialize self.completeBoard, Try calling insertNumbersToBoard first"

        firstUnblurredLocationX = 0  # Location X to be revealed first
        firstUnblurredLocationY = 0  # Location Y to be revealed first
        self.playBoard = list()  # Create playable list
        validLocations = list()

        for i in self.completeBoard:
            self.playBoard.append(i.copy())  # Play board copy complete board
        for x in range(len(self.playBoard)):
            for y in range(len(self.playBoard)):
                self.playBoard[x][y] = " "  # Change every tile in playboard to " "

        for x in range(self.yDimen):
            for y in range(self.xDimen):
                if self.completeBoard[x][y] == "0":
                    validLocations.append((x, y))
        if len(validLocations) == 0:
            print("No valid locations to reveal. The board might be all mines!")
            return self.playBoard
        firstUnblurredLocationX, firstUnblurredLocationY = random.choice(validLocations)
        self.playBoard[firstUnblurredLocationY][firstUnblurredLocationX] = "0"
        return self.playBoard

    def updateBoard(self, choiceX, choiceY, changeTo):
        self.playBoard[choiceY][choiceX] = changeTo

    def returnPlayBoard(self):
        return self.playBoard  # Return playboard

    def returnCompleteBoard(self):
        return self.completeBoard  # Return complete board with numbers


