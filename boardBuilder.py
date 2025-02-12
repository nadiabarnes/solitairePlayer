import pydealer
from pydealer.const import TOP, BOTTOM

class solitaireTable(object):
    """manages the cards on the board, moves cards, determines if you are allowed to move a card"""
    #the "top" of a stack is the last index. when you "deal" a card, it puts the top card
    #from the delt deck onto the top of the target deck

    def __init__(self):
        """will need to have a deck of "cards" that is randomly distributed into the pile and buildstacks"""
        deck = pydealer.Deck()
        deck.shuffle()
        self.deck = deck
        self.newRanks = {
                "King": 13,"Queen": 12,"Jack": 11,"10": 10,"9": 9,
                "8": 8,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 2,"Ace": 1}
        #four elements, that go up numerically when you move a card onto them
        self.suitStacks = ([pydealer.Stack(),pydealer.Stack(),
                            pydealer.Stack(),pydealer.Stack()])
        #starts empty
        self.talon = pydealer.Stack()
        #pile contains 24 cards at start
        pile = pydealer.Stack()
        pile.add(deck.deal(24))
        self.pile = pile
        #list of stacks, each list index is one of the buildStacks. first index as one card, etc
        buildStacks = [None] * 7
        for i in range(0,7):
            buildStacks[i] = pydealer.Stack()
            buildStacks[i].add(deck.deal(i+1))
        self.buildStacks = buildStacks
        #what is the index of the highest visable card in each of the buildstacks.
        #basically, how far are you allowed to look into the queue
        self.visable = [0, 1, 2, 3, 4, 5, 6]

    def __repr__(self):
        """eventually will pretty print the current view of the board.
        tested = true"""
        result = ""
        #first line is num in pile and top of talon
        talonvar = "| |"
        if len(self.talon) > 0:
            talonvar = "|"+str(self.talon[len(self.talon)-1])+"|"
        result = "|"+str(len(self.pile))+"|  "+talonvar+"\n"
        #2nd line is the four suit stacks
        for i in range(0,4):
            if len(self.suitStacks[i])>0:
                result=result+"|"+str(self.suitStacks[i][len(self.suitStacks[i])-1])+"|  "
            else: result = result+"| |  "
        #next lines are the build stacks, starting with 7 going down to 1
        for i in range(6,-1,-1):
            result = result+"\n"  
            if len(self.buildStacks[i])>0:
                result=result+str(i+1)+": "
                for j in range(len(self.buildStacks[i])-1,-1,-1):
                    result = result+"|"+str(self.buildStacks[i][j])+"| "
            else: result=result+str(i+1)+": "+"| |"
        return result

    def validBuildStack(self, movedCard=pydealer.Card, targetCard=pydealer.Card):
        """checks if you can move a card onto one of the buildstacks.
        Moved card is the card you want to move, targetCard is the 
        one you want to attach it to. Checks the validity of the suits and the value.
        Returns true if you can move it.
        tested = false"""
        if movedCard.suit == "Clubs" or movedCard.suit == "Spades":
            if targetCard.suit == "Hearts" or targetCard.suit == "Diamonds":
                return self.newRanks.get(movedCard.value) == self.newRanks.get(targetCard.value)-1
            else: return False
        elif targetCard.suit == "Clubs" or targetCard.suit == "Spades":
            return self.newRanks.get(movedCard.value) == self.newRanks.get(targetCard.value)-1
        else: return False
        
    def validSuitStack(self, movedCard=pydealer.Card, targetDeck = pydealer.Stack):
        """checks if you can move a card onto a suitStack. returns true if you can.
        tested = false"""
        if len(targetDeck)+1 == self.newRanks.get(movedCard.value):
            return True

    def resetPile(self):
        """flip the talon over to the pile
        tested = true"""
        if len(self.talon) > 0 and len(self.pile) == 0:
            self.pile.add(self.talon.deal(len(self.talon)))
        else: print("Invalid Pile Reset")

    def moveBuildStack(self, movedStack=pydealer.Stack(), movedCardDepth=int, targetStack=pydealer.Stack):
        """move one section from the build stack to another location in the buildstack
        tested=True"""
        if self.validBuildStack(movedStack[movedCardDepth], targetStack[0]) == True:
            holdStack=pydealer.Stack()
            holdStack.add(movedStack[:(movedCardDepth+1)])
            holdStack.reverse()
            targetStack.add(holdStack, end=BOTTOM)
            movedStack.cards = [card for card in movedStack.cards if card not in holdStack.cards]
        else: print("Invalid to move " + str(movedStack[movedCardDepth]) + " to " + str(targetStack[0]))

    def flipPile(self):
        """reveal the next card in the pile by flipping it to the talon
        Tested = true"""
        if len(self.pile) > 0:
            self.talon.add(self.pile.deal(1))
        else: self.resetPile()

    def moveTalon(self, targetStack=pydealer.Stack):
        """move the current talon card into one of the buildStacks
        tested = false"""
        if len(self.talon) > 0:
            if self.validBuildStack(self.talon[len(self.talon)-1], targetStack[len(targetStack)-1]) == True:
                targetStack.add(self.talon.deal(1))
            else:print("Invalid to move " + str(self.talon[len(self.talon)-1]) + " to " + str(targetStack[len(targetStack)-1]))
        else: print("Invalid move")
        
    def movetoSuitStack(self, movedStack=pydealer.Stack(),targetStackIndex=int):
        """move a card from buildStack to suitStack by specifying which buildstack
        tested=true"""
        #could add feature to recognize what suit stack automatically rather than as input
        if self.validSuitStack(movedStack[0], self.suitStacks[targetStackIndex])==True:
            self.suitStacks[targetStackIndex].add(movedStack[0])
            del movedStack.cards[0]
        else: print("Invalid to move " + str(movedStack[0]) + " to suitstack " + str(targetStackIndex))

    def moveFromSuitStack(self, movedStack=pydealer.Stack(),targetStackIndex=int):
        """move a card from a suitstack into a buildStack
        tested = false"""
        if self.validBuildStack(movedStack[0], self.buildStacks[targetStackIndex][0])==True:
            self.buildStacks[targetStackIndex].add(movedStack[0], end = BOTTOM)
            del movedStack.cards[0]
        else: print("Invalid to move " + str(movedStack[0]) + " to buildstack " + str(targetStackIndex[0]))

#----------------------------------------
##testing section##
#----------------------------------------
#testBoard = solitaireTable()
#print(testBoard)
#testBoard.moveBuildStack(testBoard.buildStacks[2], 2, testBoard.buildStacks[3])
#print(testBoard.buildStacks[6][0])


