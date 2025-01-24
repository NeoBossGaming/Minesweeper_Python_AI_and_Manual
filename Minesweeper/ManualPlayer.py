from Controller import GameController
import os
def printBoard(controller):
    index = 0
    print("  ", end = "  ")
    for i in range(len(controller.showBoard())):
        print(i, end = "    ")
    print("")
    for i in controller.showBoard():
        print(index, end = " ")
        print(i)
        index +=1


def runGamePlayer(difficulty, name):
    os.system("cls")
    controller = GameController(difficulty)
    score = 0
    print(f"Hello {name}") # Print Introduction
    print("Your Board: ")
    printBoard(controller)
    continueChoice = int(input("Would you like the proceed? 1 = Yes, 2 = Change Board, 3 = Leave : ")) # Validate if willing to proceed
    if continueChoice not in [1,2,3]:
        print("Invalid, Ending Game")
        return
    if continueChoice == 1: # Continue Game
        while True:
            os.system("cls")
            printBoard(controller)
            print("What would you like to do")
            choice = int(input("1(Reveal) 2(Flag) 3(UnFlag) 4(Leave)"))
            if choice == 4:
                leave = input("Are you sure you want to leave, 1 = Leave 2 = Stay?")
                if leave == "1":
                    return score
                if leave == "2":
                    pass
            locationX = int(input("Enter Horizontal Location(Most Left is 0)"))
            locationY = int(input("Enter Vertical Location(Most Up is 0)"))
            revealed = controller.executeAction(choice, locationX, locationY)
            if revealed == "9":
                os.system("clear")
                # Lost
                print(f"You have lost, you stepped on a mine {name}")
                printBoard(controller)
                return score
            elif revealed == "End":
                return score
            os.system("cls")
            printBoard(controller)
            score += 1
            if controller.checkIfWin():
                os.system("cls")
                print(f"Congratulations you have won {name}!")
                print(f"Your total score is: {score}")
            input("To Continue, Press Enter")
    if continueChoice == 2: # Restart Game
        runGamePlayer(difficulty, name)
        return
    if continueChoice == 3: # Leave
        return
