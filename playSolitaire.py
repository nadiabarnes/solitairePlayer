import boardBuilder

#username = input("Enter username:")
#print("Username is: " + username)
def main():
    print("-----------------------------------------------------------------------------")
    print("This solitaire is being tested, so please be patient with the UI! Prompts are case sensitive.")
    print("-----------------------------------------------------------------------------")
    playStatus = int(input("Would you like to play solitaire? 1=Yes or 0=No: "))
    board = boardBuilder.solitaireTable()
    while playStatus == 1:
        print(board)
        print("1: Flip Pile | 2: Move a buildstack card | 3: Move the talon card | 4: Move a card to suitstack | 5: Move a card from the suit stack | 6: New Board | 7: Quit")
        move = int(input("1/2/3/4/5/6/7: "))
        if move == 1:
            #Working
            board.flipPile()
        elif move == 2:
            #Working
            movedCardStack = int(input("For the moving card, which stack? (1-7): "))
            movedCardDepth = int(input("For the moving card, how deep? (far right is 0): "))
            targetCardStack = int(input("For the target card, which stack? (1-7): "))
            #TODO make this method call easier
            board.moveBuildStack(board.buildStacks[movedCardStack-1], movedCardDepth, board.buildStacks[targetCardStack-1])
        elif move == 3:
            #Working
            targetCardStack = int(input("For the target card, which stack? (1-7): "))
            #TODO make this method call easier
            board.moveTalon(board.buildStacks[targetCardStack-1])
        elif move ==4:
            #Working
            movedCardStack = int(input("For the moving card, which stack? (1-7): "))
            targetCardStack = int(input("For the target stack, which stack? (1-4): "))
            #TODO make this method call easier
            board.movetoSuitStack(board.buildStacks[movedCardStack-1], targetCardStack-1)
        elif move == 5:
            #Working
            movedCardStack = int(input("For the moving card, which stack? (1-4): "))
            targetCardStack = int(input("For the target stack, which stack? (1-7): "))
            #TODO make this method call easier
            board.moveFromSuitStack(board.suitStacks[movedCardStack-1], targetCardStack-1)
        elif move == 6:
            board = boardBuilder.solitaireTable()
        elif move == 7:
            playStatus = 0
        else: print("Invalid Move Input")
        print("-----------------------------------------------------------------------------")

main()
