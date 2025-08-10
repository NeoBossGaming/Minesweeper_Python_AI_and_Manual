from Controller import GameController
import random
def printBoard(controller):
    index = 0
    print("  ", end = "   ")
    for i in range(controller.playBoard.xDimen):
        if i < 10:
            print(i, end="    ")
        else:
            print(i, end="   ")
    print("")
    for i in controller.showBoard():
        if index < 10:
            print(index, end = "  ")
            print(i)
            index +=1
        else:
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
                if controller.showBoard()[y][x] == " ":
                    isFound = True
                if controller.showBoard()[y][x] == "9":
                    return False
        if isFound == True:
            continue
        else:
            if checkWin(controller, controller.showBoard(), controller.completeBoard):
                return True
            else:
                printBoard(controller)
                return False

def checkWin(controller, playBoard, completeBoard):
    foundLoosingEvidence = False
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if playBoard[y][x] == completeBoard[y][x]:
                continue
            elif playBoard[y][x] == "F" and completeBoard[y][x] == "9":
               continue
            else:
                foundLoosingEvidence = True
    return not foundLoosingEvidence

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
                if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
                    if board[i[1]][i[0]] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                        surroundingCordsAmount += 1
                if surroundingCordsAmount == 7 :
                    for i in surCords:
                        if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
                            if board[i[1]][i[0]] == " ":
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
        if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
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
        if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
            if board[i[1]][i[0]] == " " or board[i[1]][i[0]] == "F":
                surroundingtile += 1
    return surroundingtile
def checkForTileNumberSurpassingFlaggedSurrounding(board, controller):
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if board[y][x] == " " or board[y][x] == "F":
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
                    if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
                        if board[i[1]][i[0]] == " ":
                            location = {
                                "Action" : 1,
                                "XLoc" : i[0],
                                "YLoc" : i[1]
                            }
                            return location
    return None

def pattern1_1(board, controller):
    # When in a corner, there is a 1, and next to it is another 1
    # In that case, the one further from the corner, we can open it
    # |      <--- Open
    # |1 1 1 1 1

    # List of locations that can be opened
    possibleLocations = list()

    # Detect 1 - 1 Pattern
    # Once detected, add that one

    # Detect in edge
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):

            # On edges
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][0] == "1" and board[y][1] == "1" and not board[y - 1][1] in ["F", " "] and not board[y - 1][0] in ["F", " "]:
                if board[y + 1][1] == " " and board[y + 1][0] == " " and board[y + 1][2] == " ":
                    possibleLocations.append((2, y + 1))
            # Vertically Up
            if  y != 0 and y != controller.playBoard.yDimen - 1 and board[y][0] == "1" and board[y][1] == "1" and not board[y + 1][1] in ["F", " "] and not board[y + 1][0] in ["F", " "]:
                if board[y - 1][1] == " " and board[y - 1][0] == " " and board[y - 1][2] == " ":
                    possibleLocations.append((2, y - 1))

            # Right side of board
            # Vertically Down
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][controller.playBoard.xDimen - 1] == "1" and board[y][controller.playBoard.xDimen - 2] == "1" and not board[y - 1][controller.playBoard.xDimen - 1] in ["F", " "] and not board[y - 1][controller.playBoard.xDimen - 2] in ["F", " "]:
                if board[y + 1][controller.playBoard.xDimen - 1] == " " and board[y + 1][controller.playBoard.xDimen - 2] == " " and board[y + 1][controller.playBoard.xDimen - 3] == " ":
                    possibleLocations.append((controller.playBoard.xDimen - 3, y + 1))
            # Vertically Up
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][controller.playBoard.xDimen - 1] == "1" and board[y][controller.playBoard.xDimen - 2] == "1" and not board[y + 1][controller.playBoard.xDimen - 1] in ["F", " "] and not board[y + 1][controller.playBoard.xDimen - 2] in ["F", " "]:
                if board[y - 1][controller.playBoard.xDimen - 1] == " " and board[y - 1][controller.playBoard.xDimen - 2] == " " and board[y - 1][controller.playBoard.xDimen - 3] == " ":
                    possibleLocations.append((controller.playBoard.xDimen - 3, y - 1))

            # Up side of board
            # Horizontally Right
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[0][x] == "1" and board[1][x] == "1" and not board[1][x - 1] in ["F", " "] and not board[0][x - 1] in ["F", " "]:
                if board[0][x + 1] == " " and board[1][x + 1] == " " and board[2][x + 1] == " ":
                    possibleLocations.append((x + 1, 2))
            # Horizontally Left
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[0][x] == "1" and board[1][x] == "1" and not board[1][x + 1] in ["F", " "] and not board[0][x + 1] in ["F", " "]:
                if board[0][x - 1] == " " and board[1][x - 1] == " " and board[2][x - 1] == " ":
                    possibleLocations.append((x - 1, 2))

            # Down side of board
            # Horizontally Left
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[controller.playBoard.yDimen - 1][x] == "1" and board[controller.playBoard.yDimen - 2][x] == "1" and not board[controller.playBoard.yDimen - 2][x + 1] in ["F", " "] and not board[controller.playBoard.yDimen - 1][x + 1] in ["F", " "]:
                if board[controller.playBoard.yDimen - 1][x - 1] == " " and board[controller.playBoard.yDimen - 2][x - 1] == " " and board[controller.playBoard.yDimen - 3][x - 1] == " ":
                    possibleLocations.append((x - 1, controller.playBoard.yDimen - 3))
            # Horizontally Right
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[controller.playBoard.yDimen - 1][x] == "1" and board[controller.playBoard.yDimen - 2][x] == "1" and not board[controller.playBoard.yDimen - 2][x - 1] in ["F", " "] and not board[controller.playBoard.yDimen - 1][x - 1] in ["F", " "]:
                if board[controller.playBoard.yDimen - 1][x + 1] == " " and board[controller.playBoard.yDimen - 2][x + 1] == " " and board[controller.playBoard.yDimen - 3][x + 1] == " ":
                    possibleLocations.append((x + 1, controller.playBoard.yDimen - 3))


            # In the middle of the board

            # Facing horizontally
            if y not in [0, controller.playBoard.yDimen - 1]:  # Check y Dimensions Boundaries
                # Facing to the right
                if x not in [0, controller.playBoard.xDimen - 1, controller.playBoard.xDimen - 2]: # Check x Dimensions Boundaries
                    if board[y][x] == "1" and board[y][x + 1] == "1": # Find if 1 - 1
                        # Vertically Up
                        if board[y + 1][x] not in ["F", " "] and board[y + 1][x + 1] not in ["F", " "]: # Check boxes below
                            if board[y - 1][x - 1] not in ["F", " "] and board[y][x - 1] not in ["F", " "] and board[y + 1][x - 1] not in ["F", " "]: # Check boxes in the left of it
                                if board[y - 1][x] == " " and board[y - 1][x + 1] == " " and board[y - 1][x + 2] == " ":
                                    possibleLocations.append((x + 2, y - 1))

                        # Vertically Down
                        if board[y - 1][x] not in ["F", " "] and board[y - 1][x + 1] not in ["F", " "]: # Check boxes above
                            if board[y - 1][x - 1] not in ["F", " "] and board[y][x - 1] not in ["F", " "] and board[y + 1][x - 1] not in ["F", " "]: # Check boxes in the left of it
                                if board[y + 1][x] == " " and board[y + 1][x + 1] == " " and board[y + 1][x + 2] == " ":
                                    possibleLocations.append((x + 2, y + 1))

                # Facing to the left
                if x not in [0, 1, controller.playBoard.xDimen - 1]: # Check x Dimensions Boundaries
                    if board[y][x] == "1" and board[y][x - 1] == "1":  # Find if 1 - 1
                        # Vertically Up
                        if board[y + 1][x] not in ["F", " "] and board[y + 1][x - 1] not in ["F", " "]:  # Check boxes below
                            if board[y - 1][x + 1] not in ["F", " "] and board[y][x - 1] not in ["F", " "] and \
                                    board[y + 1][x + 1] not in ["F", " "]:  # Check boxes in the right of it
                                if board[y - 1][x] == " " and board[y - 1][x - 1] == " " and board[y - 1][x - 2] == " ":
                                    possibleLocations.append((x - 2, y - 1))

                        # Vertically Down
                        if board[y - 1][x] not in ["F", " "] and board[y - 1][x - 1] not in ["F", " "]:  # Check boxes above
                            if board[y - 1][x + 1] not in ["F", " "] and board[y][x + 1] not in ["F", " "] and board[y + 1][x + 1] not in ["F", " "]:  # Check boxes in the left of it
                                if board[y + 1][x] == " " and board[y + 1][x - 1] == " " and board[y + 1][x - 2] == " ":
                                    possibleLocations.append((x - 2, y + 1))

            # Facing Vertically
            if x not in [0, controller.playBoard.xDimen - 1]: # Checking x Dimensions
                # Facing to the up
                if y not in [0, 1, controller.playBoard.yDimen - 1]:
                    if board[y][x] == "1" and board[y - 1][x] == "1": # Find if 1 - 1
                        # Horizontally Left
                        if board[y][x + 1] not in ["F", " "] and board[y - 1][x + 1] not in ["F", " "]: # Check boxes in the right
                            if board[y + 1][x + 1] not in ["F", " "] and board[y + 1][x] not in ["F", " "] and board[y + 1][x - 1] not in ["F", " "]: # Check boxes below it
                                if board[y][x - 1] == " " and board[y - 1][x - 1] == " " and board[y - 2][x - 1] == " ":
                                    possibleLocations.append((x - 1, y - 2))
                        # Horizontally Right
                        if board[y][x - 1] not in ["F", " "] and board[y - 1][x - 1] not in ["F", " "]:  # Check boxes in the left
                            if board[y + 1][x - 1] not in ["F", " "] and board[y + 1][x] not in ["F", " "] and board[y + 1][x + 1] not in ["F", " "]: # Check boxes below it
                                if board[y][x + 1] == " " and board[y - 1][x + 1] == " " and board[y - 2][x + 1] == " ":
                                    possibleLocations.append((x + 1, y - 2))
                # Facing to the down
                if y not in [0, controller.playBoard.yDimen - 1, controller.playBoard.yDimen - 2]:
                    if board[y][x] == "1" and board[y + 1][x] == "1":
                        # Horizontally Left
                        if board[y][x + 1] not in ["F", " "] and board[y + 1][x + 1] not in ["F", " "]: # Check boxes in the right
                            if board[y - 1][x + 1] not in ["F", " "] and board[y - 1][x] not in ["F", " "] and board[y - 1][x - 1] not in ["F", " "]: # Check boxes below it
                                if board[y][x - 1] == " " and board[y + 1][x - 1] == " " and board[y + 2][x - 1] == " ":
                                    possibleLocations.append((x - 1, y + 2))

                        # Horizontally Right
                        if board[y][x - 1] not in ["F", " "] and board[y + 1][x - 1] not in ["F", " "]: # Check boxes in the left
                            if board[y - 1][x - 1] not in ["F", " "] and board[y - 1][x] not in ["F", " "] and board[y - 1][x + 1] not in ["F", " "]: # Check boxes below it
                                if board[y][x + 1] == " " and board[y + 1][x + 1] == " " and board[y + 2][x + 1] == " ":
                                    possibleLocations.append((x + 1, y + 2))
    if len(possibleLocations) == 0:
        return None
    luckyChoice = random.choice(possibleLocations)
    location = {
        "Action": 1,
        "XLoc": luckyChoice[0],
        "YLoc": luckyChoice[1]
    }
    return location

def pattern1_2(board, controller):
    # When in a corner, there is a 1, and next to it is another 1
    # In that case, the one further from the corner, we can open it
    # |      <--- Open
    # |1 1 1 1 1

    # List of locations that can be opened
    possibleLocations = list()

    # Detect 1 - 1 Pattern
    # Once detected, add that one

    # Detect in edge
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            # Left side of the board
            # Vertically Down
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][0] == "1" and board[y][1] == "2" and not \
            board[y - 1][1] in ["F", " "] and not board[y - 1][0] in ["F", " "] and not board[y - 1][2] in ["F", " "] and not board[y][2] in ["F", " "]:
                if board[y + 1][1] == " " and board[y + 1][0] == " " and board[y + 1][2] == " ":
                    possibleLocations.append((2, y + 1))
            # Vertically Up
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][0] == "1" and board[y][1] == "2" and not \
            board[y + 1][1] in ["F", " "] and not board[y + 1][0] in ["F", " "] and not board[y + 1][2] in ["F", " "] and not board[y][2] in ["F", " "]:
                if board[y - 1][1] == " " and board[y - 1][0] == " " and board[y - 1][2] == " ":
                    possibleLocations.append((2, y - 1))

            # Right side of board
            # Vertically Down
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][
                controller.playBoard.xDimen - 1] == "1" and board[y][controller.playBoard.xDimen - 2] == "2" and not \
            board[y - 1][controller.playBoard.xDimen - 1] in ["F", " "] and not board[y - 1][controller.playBoard.xDimen - 2] in ["F", " "] and not board[y - 1][controller.playBoard.xDimen - 3] in ["F", " "] and not board[y][controller.playBoard.xDimen - 3] in ["F", " "]:
                if board[y + 1][controller.playBoard.xDimen - 1] == " " and board[y + 1][controller.playBoard.xDimen - 2] == " " and \
                        board[y + 1][controller.playBoard.xDimen - 3] == " ":
                    possibleLocations.append((controller.playBoard.xDimen - 3, y + 1))
            # Vertically Up
            if y != 0 and y != controller.playBoard.yDimen - 1 and board[y][
                controller.playBoard.xDimen - 1] == "1" and board[y][controller.playBoard.xDimen - 2] == "2" and not \
            board[y + 1][controller.playBoard.xDimen - 1] in ["F", " "] and not board[y + 1][controller.playBoard.xDimen - 2] in ["F", " "] and not board[y + 1][controller.playBoard.xDimen - 3] in ["F", " "] and not board[y + 1][controller.playBoard.xDimen - 3] in ["F", " "] and not board[y][controller.playBoard.xDimen - 3] in ["F", " "]:
                if board[y - 1][controller.playBoard.xDimen - 1] == " " and board[y - 1][
                    controller.playBoard.xDimen - 2] == " " and board[y - 1][
                    controller.playBoard.xDimen - 3] == " ":
                    possibleLocations.append((controller.playBoard.xDimen - 3, y - 1))

            # Up side of board
            # Horizontally Right
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[0][x] == "1" and board[1][x] == "2" and not \
            board[1][x - 1] in ["F", " "] and not board[0][x - 1] in ["F", " "] and not board[2][x - 1] in ["F", " "] and not board[2][x] in ["F", " "]:
                if board[0][x + 1] == " " and board[1][x + 1] == " " and board[2][x + 1] == " ":
                    possibleLocations.append((x + 1, 2))
            # Horizontally Left
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[0][x] == "1" and board[1][x] == "2" and not \
            board[1][x + 1] in ["F", " "] and not board[0][x + 1] in ["F", " "] and not board[2][x + 1] in ["F", " "] and not board[2][x] in ["F", " "]:
                if board[0][x - 1] == " " and board[1][x - 1] == " " and board[2][x - 1] == " ":
                    possibleLocations.append((x - 1, 2))

            # Downside of board
            # Horizontally Left
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[controller.playBoard.yDimen - 1][
                x] == "1" and board[controller.playBoard.yDimen - 2][x] == "2" and not \
            board[controller.playBoard.yDimen - 2][x + 1] in ["F", " "] and not \
            board[controller.playBoard.yDimen - 1][x + 1] in ["F", " "] and not board[controller.playBoard.yDimen - 3][x + 1] in ["F", " "] and not board[controller.playBoard.yDimen - 3][x] in ["F", " "]:
                if board[controller.playBoard.yDimen - 1][x - 1] == " " and board[controller.playBoard.yDimen - 2][
                    x - 1] == " " and board[controller.playBoard.yDimen - 3][x - 1] == " ":
                    possibleLocations.append((x - 1, controller.playBoard.yDimen - 3))
            # Horizontally Right
            if x != 0 and x != controller.playBoard.xDimen - 1 and board[controller.playBoard.yDimen - 1][
                x] == "1" and board[controller.playBoard.yDimen - 2][x] == "2" and not \
            board[controller.playBoard.yDimen - 2][x - 1] in ["F", " "] and not \
            board[controller.playBoard.yDimen - 1][x - 1] in ["F", " "] and not board[controller.playBoard.yDimen - 3][x - 1] in ["F", " "] and not board[controller.playBoard.yDimen - 3][x] in ["F"," "]:
                if board[controller.playBoard.yDimen - 1][x + 1] == " " and board[controller.playBoard.yDimen - 2][
                    x + 1] == " " and board[controller.playBoard.yDimen - 3][x + 1] == " ":
                    possibleLocations.append((x + 1, controller.playBoard.yDimen - 3))

            # In the middle of the board

            # Facing horizontally
            if y not in [0, controller.playBoard.yDimen - 1]:  # Check y Dimensions Boundaries

                # Facing to the right
                if x not in [0, controller.playBoard.xDimen - 1,
                             controller.playBoard.xDimen - 2]:  # Check x Dimensions Boundaries
                    if board[y][x] == "1" and board[y][x + 1] == "2":  # Find if 1 - 2
                        # Vertically Up
                        if board[y + 1][x] not in ["F", " "] and board[y + 1][x + 1] not in ["F", " "] and not board[y + 1][x + 2] in ["F", " "] and not board[y][x + 2] in ["F", " "]:  # Check boxes below
                            if board[y - 1][x - 1] not in ["F", " "] and board[y][x - 1] not in ["F", " "] and \
                                    board[y + 1][x - 1] not in ["F", " "]:  # Check boxes in the left of it
                                if board[y - 1][x] == " " and board[y - 1][x + 1] == " " and board[y - 1][
                                    x + 2] == " ":
                                    possibleLocations.append((x + 2, y - 1))

                        # Vertically Down
                        if board[y - 1][x] not in ["F", " "] and board[y - 1][x + 1] not in ["F", " "] and not board[y - 1][x + 2] in ["F", " "] and not board[y][x + 2] in ["F", " "]:  # Check boxes above
                            if board[y - 1][x - 1] not in ["F", " "] and board[y][x - 1] not in ["F", " "] and \
                                    board[y + 1][x - 1] not in ["F", " "]:  # Check boxes in the left of it
                                if board[y + 1][x] == " " and board[y + 1][x + 1] == " " and board[y + 1][
                                    x + 2] == " ":
                                    possibleLocations.append((x + 2, y + 1))

                # Facing to the left
                if x not in [0, 1, controller.playBoard.xDimen - 1]:  # Check x Dimensions Boundaries
                    if board[y][x] == "1" and board[y][x - 1] == "2":  # Find if 1 - 2
                        # Vertically Up
                        if board[y + 1][x] not in ["F", " "] and board[y + 1][x - 1] not in ["F", " "] and not board[y + 1][x - 2] in ["F", " "] and not board[y][x - 2] in ["F", " "]:  # Check boxes below
                            if board[y - 1][x + 1] not in ["F", " "] and board[y][x - 1] not in ["F", " "] and \
                                    board[y + 1][x + 1] not in ["F", " "]:  # Check boxes in the right of it
                                if board[y - 1][x] == " " and board[y - 1][x - 1] == " " and board[y - 1][
                                    x - 2] == " ":
                                    possibleLocations.append((x - 2, y - 1))

                        # Vertically Down
                        if board[y - 1][x] not in ["F", " "] and board[y - 1][x - 1] not in ["F", " "] and not board[y - 1][x - 2] in ["F", " "] and not board[y][x - 2] in ["F", " "]:  # Check boxes above
                            if board[y - 1][x + 1] not in ["F", " "] and board[y][x + 1] not in ["F", " "] and \
                                    board[y + 1][x + 1] not in ["F", " "]:  # Check boxes in the left of it
                                if board[y + 1][x] == " " and board[y + 1][x - 1] == " " and board[y + 1][
                                    x - 2] == " ":
                                    possibleLocations.append((x - 2, y + 1))

            # Facing Vertically
            if x not in [0, controller.playBoard.xDimen - 1]:  # Checking x Dimensions
                # Facing to the up
                if y not in [0, 1, controller.playBoard.yDimen - 1]:
                    if board[y][x] == "1" and board[y - 1][x] == "2":  # Find if 1 - 1
                        # Horizontally Left
                        if board[y][x + 1] not in ["F", " "] and board[y - 1][x + 1] not in ["F", " "] and not board[y - 2][x + 1] in ["F", " "] and not board[y - 2][x] in ["F", " "]:  # Check boxes in the right
                            if board[y + 1][x + 1] not in ["F", " "] and board[y + 1][x] not in ["F", " "] and \
                                    board[y + 1][x - 1] not in ["F", " "]:  # Check boxes below it
                                if board[y][x - 1] == " " and board[y - 1][x - 1] == " " and board[y - 2][
                                    x - 1] == " ":
                                    possibleLocations.append((x - 1, y - 2))
                        # Horizontally Right
                        if board[y][x - 1] not in ["F", " "] and board[y - 1][x - 1] not in ["F", " "] and not board[y - 2][x - 1] in ["F", " "] and not board[y - 2][x] in ["F", " "]:  # Check boxes in the left
                            if board[y + 1][x - 1] not in ["F", " "] and board[y + 1][x] not in ["F", " "] and \
                                    board[y + 1][x + 1] not in ["F", " "]:  # Check boxes below it
                                if board[y][x + 1] == " " and board[y - 1][x + 1] == " " and board[y - 2][
                                    x + 1] == " ":
                                    possibleLocations.append((x + 1, y - 2))
                # Facing to the down
                if y not in [0, controller.playBoard.yDimen - 1, controller.playBoard.yDimen - 2]:
                    if board[y][x] == "1" and board[y + 1][x] == "2":
                        # Horizontally Left
                        if board[y][x + 1] not in ["F", " "] and board[y + 1][x + 1] not in ["F", " "] and not board[y + 2][x + 1] in ["F", " "] and not board[y + 2][x] in ["F", " "]:  # Check boxes in the right
                            if board[y - 1][x + 1] not in ["F", " "] and board[y - 1][x] not in ["F", " "] and \
                                    board[y - 1][x - 1] not in ["F", " "]:  # Check boxes below it
                                if board[y][x - 1] == " " and board[y + 1][x - 1] == " " and board[y + 2][
                                    x - 1] == " ":
                                    possibleLocations.append((x - 1, y + 2))

                        # Horizontally Right
                        if board[y][x - 1] not in ["F", " "] and board[y + 1][x - 1] not in ["F",  " "] and not board[y + 2][x - 1] in ["F", " "] and not board[y + 2][x] in ["F", " "]:  # Check boxes in the left
                            if board[y - 1][x - 1] not in ["F", " "] and board[y - 1][x] not in ["F", " "] and \
                                    board[y - 1][x + 1] not in ["F", " "]:  # Check boxes below it
                                if board[y][x + 1] == " " and board[y + 1][x + 1] == " " and board[y + 2][
                                    x + 1] == " ":
                                    possibleLocations.append((x + 1, y + 2))

    if len(possibleLocations) == 0:
        return None
    luckyChoice = random.choice(possibleLocations)
    location = {
        "Action": 2,
        "XLoc": luckyChoice[0],
        "YLoc": luckyChoice[1]
    }

    return location
def checkForMineSurroundingTile(board, controller):
    for y in range(controller.playBoard.yDimen):
        for x in range(controller.playBoard.xDimen):
            if board[y][x] == " " or board[y][x] == "F":
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
                    if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
                        if board[i[1]][i[0]] == " ":
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
            if board[y][x] == " ":
                continue

            surCords = [
                (x - 1, y), (x + 1, y),
                (x, y + 1), (x, y - 1),
                (x + 1, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x - 1, y - 1)
            ]

            for i in surCords:
                if 0 <= i[0] < controller.playBoard.xDimen and 0 <= i[1] < controller.playBoard.yDimen:
                    if board[i[1]][i[0]] == " ":
                        possibleLocations.append((i[0], i[1]))

    if len(possibleLocations) == 0:
        return None
    luckyChoice = random.choice(possibleLocations)

    location = {
        "Action": 1,
        "XLoc": luckyChoice[0],
        "YLoc": luckyChoice[1]
    }
    return location

def makeChoice(board, controller):

    cornerCheck = findCorner(board, controller)
    if cornerCheck is not None:
        return cornerCheck

    tileNumCheck = checkForTileNumberSurpassingFlaggedSurrounding(board, controller)
    if tileNumCheck is not None:
        return tileNumCheck

    tileSurCheck = checkForMineSurroundingTile(board, controller)
    if tileSurCheck is not None:
        return tileSurCheck

    firstPattern = pattern1_1(board,controller)
    if firstPattern is not None:
        return firstPattern

    secondPattern = pattern1_2(board,controller)
    if secondPattern is not None:
        return secondPattern

    # Randomizer
    randomizerFunction = randomizer(board,controller)
    if randomizerFunction is not None:
        return randomizerFunction

