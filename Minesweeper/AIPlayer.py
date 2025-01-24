from Controller import GameController
import random

def printBoard(controller):
    index = 0
    print("  ", end = "   ")
    for i in range(len(controller.showBoard())):
        print(i, end = "    ")
    print("")
    for i in controller.showBoard():
        print(index, end = " ")
        print(i)
        index +=1

def runGame(difficulty):
    # os.system("cls")
    controller = GameController(difficulty)
    score = 0
    moves = 0
    while True:
        choiceDetails = makeChoice(controller.showBoard(), controller)
        if choiceDetails is not None:
            controller.executeAction(choiceDetails["Action"], choiceDetails["XLoc"], choiceDetails["YLoc"])
        moves += 1
        if difficulty == 1 and moves == 101:
            break
        elif difficulty == 2 and moves == 257:
            break
        elif difficulty == 3 and moves == 401:
            break
        isFound = False
        for y in range(controller.playBoard.yDimen):
            for x in range(controller.playBoard.xDimen):
                if controller.showBoard()[y][x] == "?":
                    isFound = True
                if controller.showBoard()[y][x] == "9":
                    return False


        if isFound == True:
            # print("Nah I'd Win")
            continue
        else:
            # print("Ok fine you won")
            return True


def findCorner(board, controller):
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if board[y][x] != "1":
                continue
            surCords = [
                (x - 1, y), (x + 1, y),
                (x, y + 1), (x, y - 1),
                (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
            ]
            surroundingCordsAmount = 0
            for i in surCords:
                if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
                    if board[i[1]][i[0]] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                        surroundingCordsAmount += 1
                if surroundingCordsAmount == 7 :
                    for i in surCords:
                        if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
                            if board[i[1]][i[0]] == "?":
                                location = {
                                    "Action" : 2,
                                    "XLoc" : i[0],
                                    "YLoc" : i[1]
                                }
                                return location
    return None

def findMinesSurroundingTile(board, controller, x, y):
    surCords = [
        (x - 1, y), (x + 1, y),
        (x, y + 1), (x, y - 1),
        (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
    ]
    surroundingMines = 0
    for i in surCords:
        if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
            if board[i[1]][i[0]] == "F":
                surroundingMines += 1
    return surroundingMines

def findUnopenedTiles(board, controller, x, y):
    surCords = [
        (x - 1, y), (x + 1, y),
        (x, y + 1), (x, y - 1),
        (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
    ]
    surroundingtile = 0
    for i in surCords:
        if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
            if board[i[1]][i[0]] == "?" or board[i[1]][i[0]] == "F":
                surroundingtile += 1
    return surroundingtile

    return None
def checkForTileNumberSurpassingFlaggedSurrounding(board, controller):
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if board[y][x] == "?" or board[y][x] == "F":
                continue
            surMines = findMinesSurroundingTile(board, controller, x, y)
            tileNum = board[y][x]

            if str(surMines) == str(tileNum):

                surCords = [
                    (x - 1, y), (x + 1, y),
                    (x, y + 1), (x, y - 1),
                    (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
                ]

                for i in surCords:
                    if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
                        if board[i[1]][i[0]] == "?":
                            location = {
                                "Action" : 1,
                                "XLoc" : i[0],
                                "YLoc" : i[1]
                            }
                            return location
    return None

def checkForMineSurroundingTile(board, controller):
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if board[y][x] == "?" or board[y][x] == "F":
                continue
            surUnOpenTile = findUnopenedTiles(board, controller, x, y)
            tileNum = board[y][x]
            if str(surUnOpenTile) == str(tileNum):

                surCords = [
                    (x - 1, y), (x + 1, y),
                    (x, y + 1), (x, y - 1),
                    (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
                ]

                for i in surCords:
                    if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
                        if board[i[1]][i[0]] == "?":
                            location = {
                                "Action" : 2,
                                "XLoc" : i[0],
                                "YLoc" : i[1]
                            }
                            return location
    return None

def randomizer(board,controller):
    possibleLocations = []
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if board[y][x] == "?":
                continue
            amountOfUnopenedTilesSurrounding = findUnopenedTiles(board, controller, x, y)

            if amountOfUnopenedTilesSurrounding > 0:
                surCords = [
                    (x - 1, y), (x + 1, y),
                    (x, y + 1), (x, y - 1),
                    (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
                ]

                for i in surCords:
                    if 0 <= i[0] < controller.playBoard.yDimen and 0 <= i[1] < controller.playBoard.xDimen:
                        if board[i[1]][i[0]] == "?":
                            possibleLocations.append((i[0], i[1]))

    luckyChoice = random.choice(possibleLocations)
    if len(luckyChoice) == 0:
        return None
    location = {
        "Action": 1,
        "XLoc": luckyChoice[0],
        "YLoc": luckyChoice[1]
    }
    return location



def makeChoice(board, controller):
    printBoard(controller)
    cornerCheck = findCorner(board, controller)
    if cornerCheck is not None:
        return cornerCheck

    tileNumCheck = checkForTileNumberSurpassingFlaggedSurrounding(board, controller)
    if tileNumCheck is not None:
        return tileNumCheck

    tileSurCheck = checkForMineSurroundingTile(board, controller)
    if tileSurCheck is not None:
        return tileSurCheck

    # Randomizer
    randomizerFunction = randomizer(board,controller)
    if randomizerFunction is not None:
        return randomizerFunction