import AIPlayer
import ManualPlayer

difficulty = int(input("Select Difficulty(1, 2, or 3): "))
while difficulty not in [1, 2, 3]:
    difficulty = int(input("Select Difficulty(1, 2, or 3): "))
mode = input("Select Mode(\"Player or AI\")")
if mode == "Player":
    ManualPlayer.runGamePlayer(difficulty, "Neo")
if mode == "AI":
    score = 0
    times = int(input('How many times : '))
    for t in range(times):
         if AIPlayer.runGame(difficulty):
            score += 1
            print(f"Win    Round: {t}")
         else:
            print(f"Lost    Round: {t}")
    print(f'Your AI got {score}/{times}')
