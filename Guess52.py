import random
import time
import sys

class Card():
    def __init__(self, number, suit, position):
        self.number = number
        self.suit = suit
        self.position = position
        self.name = number + " of " + suit
        self.winningCard = False

    def returnSuit(self):
        return self.suit

    def returnNumber(self):
        return self.number

    def returnPosition(self):
        return self.position

    def returnName(self):
        return self.name

    def changePosition(self, amount):
        self.position += amount

    def isWinningCard(self):
        return self.winningCard

    def toggleWinningCard(self):
        self.winningCard = True


class Deck():
    suitTypes = ["Diamonds", "Clubs", "Hearts", "Spades"]
    numberTypes = ["Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen",
                   "King"]

    def __init__(self):
        self.deckCards = []
        counter = 0
        for indexone in Deck.suitTypes:
            for indextwo in Deck.numberTypes:
                # deckCards.add([random.choice(t), i])
                self.deckCards.append(Card(indextwo, indexone, counter))
                counter += 1
        self.numberCards = len(self.deckCards)

    def returnNumberofCards(self):
        return self.numberCards

    def resetDeck(self):
        self.deckCards=[]
        counter = 0
        for indexone in Deck.suitTypes:
            for indextwo in Deck.numberTypes:
                # deckCards.add([random.choice(t), i])
                self.deckCards.append(Card(indextwo, indexone, counter))
                counter += 1
        self.numberCards = len(self.deckCards)


    def returnDeckofCards(self):
        return self.deckCards

    def ShuffleDeck(self):
        deckCardsTemp = []
        deckCardsTemp2 = []
        for i in self.deckCards:
            deckCardsTemp.append(i)
        while len(deckCardsTemp) > 0:
            randomCard = random.choice(deckCardsTemp)
            deckCardsTemp.remove(randomCard)
            deckCardsTemp2.append(randomCard)
        self.deckCards = deckCardsTemp2

    def returnChosenCardfromPos(self, position):
        return self.deckCards[position]

    def returnChosenCardfromName(self, card_name):
        for card in self.deckCards:
            if card_name == card.returnName():
                return card

    def removeCard(self, card_name):


        for i in self.deckCards:
            if Card.returnName(i) == card_name:
                for card in self.deckCards:
                    if card.returnPosition() >= i.returnPosition():
                        card.changePosition(-1)
                self.numberCards -= 1
                self.deckCards.remove(i)

                break

    def addCard(self, number, suit, positionNewCard):
        for card in self.deckCards:
            if card.returnPosition() >= positionNewCard:
                card.changePosition(1)

        self.deckCards.insert(positionNewCard, Card(number, suit, positionNewCard))
        self.numberCards += 1

    def returnRandomCardBesidesChosen(self, sparedCardName):

        x = self.returnChosenCardfromName(sparedCardName)
        position_card = x.returnPosition()
        self.removeCard(sparedCardName)
        card_to_return = (self.returnChosenCardfromName(random.choice(self.deckCards).returnName()))
        self.addCard(x.returnNumber(), x.returnSuit(), position_card)
        if x.isWinningCard():
            self.toggleWinningConditionForSpecificCard(x.returnName())
        return card_to_return

    def toggleWinningConditionForSpecificCard(self, cardName):
        for i in self.deckCards:
            if i.returnName() == cardName:
                i.toggleWinningCard()
                break

    def moveTopCardtoBottom(self):
        topCard = self.returnChosenCardfromPos((self.returnNumberofCards() - 1))
        self.removeCard(topCard.returnName())
        self.addCard(topCard.returnNumber(), topCard.returnSuit(), 0)
        if topCard.isWinningCard():
            self.toggleWinningConditionForSpecificCard(topCard.returnName())


class Game():
    def __init__(self):
        self.defaultDeck = Deck()
        self.deck = Deck()
        self.turns = 1
        self.highscore = 0
        self.points = (len(self.deck.deckCards))
        self.gamefinished = False
        self.selectRandomWinningCard()

    def returnGameFinished(self):
        return self.gamefinished

    def returnHighscore(self):
        return self.highscore

    def returnPoints(self):
        return self.points

    def returnTurnNo(self):
        return self.turns

    def changePoints(self, amount):
        self.points += amount

    def startGame(self):
        # start new cycle of game, creating a deck and shuffling it, and selecting a winning card
        self.gamefinished = False
        self.changeDeck(Deck())
        self.deck.ShuffleDeck()
        self.turns = 1
        self.points = (len(self.deck.deckCards))
        self.selectRandomWinningCard()

    def selectRandomWinningCard(self):
        randCardpos = random.randint(0, self.deck.returnNumberofCards() - 1)
        rand_card = self.deck.returnChosenCardfromPos(randCardpos)
        self.deck.toggleWinningConditionForSpecificCard(rand_card.returnName())

    def changeDeck(self, newDeck):
        self.deck = newDeck

    def changeHighscore(self, newHighscore):
        self.highscore = newHighscore

    def increaseTurn(self, amount):
        self.turns += amount

    '''
    def shuffleCurrentDeck(self):
        self.deck.ShuffleDeck()
    '''

    def IsWinningCard(self, guess):
        return guess.isWinningCard()

    def WonGame(self):
        self.gamefinished = True
        winning_card=None
        for card in self.deck.deckCards:
            if card.isWinningCard():
                winning_card = card.returnName()
                break
        print("You win! The winning card was the %s." % winning_card)
        print("There were %s cards left in the deck, and your score was %s.\nYou had a total of "
              % (self.deck.returnNumberofCards(), self.returnPoints()) +
              "%s guesses, and you won on turn %s." % (self.returnTurnNo(), self.returnTurnNo()))
        self.updateHighscore()

    def LostGame(self):
        self.gamefinished = True
        print("You lost... sad boiz :(")
        print("There were %s cards left in the deck, and your score was %s.\nYou had a total of "
              % (self.deck.returnNumberofCards(), self.returnPoints()) +
              "%s guesses, and you won on turn %s." % (self.returnTurnNo(), self.returnTurnNo()))

    def updateHighscore(self):
        if self.returnPoints() > self.returnHighscore():
            self.highscore = self.returnPoints()
        else:
            print("sorry, you did not break your highscore of %s" % self.highscore)

    def askForReplay(self):
        while True:
            response = input("Would you like to play again, Y/N?")
            if response == "Y" or response == "y":
                print("Restarting game...")
                self.startGame()
                break
            elif response == "N" or response == "n":
                print("Thanks for playing, your highscore was %s." % self.returnHighscore())
                time.sleep(2)
                print("The game will now close.")
                time.sleep(2)
                sys.exit()
            else:
                print("Please respond with either \"Y\" or \"N\".")

    def PlayTurn(self):
        if self.deck.returnNumberofCards() ==1:
            print("there is only one card left in the deck...")
            self.WonGame()

            #terminate function here pls
        rand_number = random.randint(1, 10)
        if rand_number == 1 or rand_number == 2:
            self.helping_hand()
        if rand_number == 3 or rand_number == 4:
            self.risky_bet()
        if not self.returnGameFinished():
            while True:
                response = input("Check the top card of the deck, Y/N?\n? ")
                if response == "Y" or response == "y":
                    topCard = self.deck.returnChosenCardfromPos(self.deck.returnNumberofCards() - 1)
                    if self.IsWinningCard(topCard):
                        self.changePoints(-1)
                        self.increaseTurn(1)
                        self.WonGame()
                    else:
                        self.changePoints(-1)
                        self.increaseTurn(1)
                        self.deck.removeCard(topCard.returnName())
                        print("Too bad, the card you picked was %s."
                              % (topCard.returnName()))
                    break
                elif response == "N" or response == "n":
                    self.deck.moveTopCardtoBottom()
                    self.increaseTurn(1)
                    print("The top card has been moved to the bottom of the deck.")
                    break
                else:
                    print("Please respond with either \"Y\" or \"N\".")

    def helping_hand(self):

        while True:
            response = input("It's your lucky day! Take this chance: Remove a random card \n" +
                             "without disrupting the order of the deck, for the cost of half a point.\nY/N?\n? ")
            if response == "Y" or response == "y":
                winningCardName = "p"
                for card in self.deck.deckCards:
                    if card.isWinningCard():
                        winningCardName = card.returnName()
                        break
                removed_card_name = self.deck.returnRandomCardBesidesChosen(winningCardName).returnName()
                self.deck.removeCard(removed_card_name)
                self.changePoints(-0.5)
                print("You have chosen well. The card removed was %s." % removed_card_name)
                break
            elif response == "N" or response == "n":
                breakloop = False
                while not breakloop:
                    secondresponse = input("Are you sure you want to pass on this offer?\nY/N?\n? ")
                    if secondresponse == "Y" or secondresponse == "y":
                        print("Passing offer...")
                        breakloop = True
                    elif secondresponse == "N" or secondresponse == "n":
                        cheese = "lol wrote this in for no reason"
                        break
                    else:
                        print("Please respond with either \"Y\" or \"N\".")
                    if not breakloop:
                        break
            else:
                print("Please respond with either \"Y\" or \"N\".")

    def risky_bet(self):
        while True:
            response = input("It's your lucky day! Take this chance: Remove the top card of the deck\n" +
                             "without a penalty to your score. However, if you end up\n" +
                             "removing the winning card, you lose!\nY/N?\n? ")
            if response == "Y" or response == "y":
                topCard = self.deck.returnChosenCardfromPos(self.deck.returnNumberofCards() - 1)
                if topCard.isWinningCard():
                    self.LostGame()
                else:
                    self.deck.removeCard(topCard.returnName())
                    print("You removed the %s." % topCard.returnName())
                break
            elif response == "N" or response == "n":
                breakloop = False
                while not breakloop:
                    secondresponse = input("Are you sure you want to pass on this offer?\nY/N?\n? ")
                    if secondresponse == "Y" or secondresponse == "y":
                        breakloop = True
                        print("Passing offer...")
                    elif secondresponse == "N" or secondresponse == "n":
                        break
                    else:
                        print("Please respond with either \"Y\" or \"N\".")
                if not breakloop:
                    break
            else:
                print("Please respond with either \"Y\" or \"N\".")

    def playGame(self):
        #the playGame() function is like a main() method;
        #it is an procedure unique to the Game class
        self.startGame()
        while True:
            self.startGame()
            while not self.returnGameFinished():
                '''
                winningCardName = "p"
                for card in self.deck.deckCards:
                    if card.isWinningCard():
                        winningCardName = card.returnName()
                        break
                '''
                print("\n\n\nThe current turn is %s. "
                      "" % self.returnTurnNo() +
                      "There are %s cards left in the deck. " % self.deck.returnNumberofCards() +
                      "Your score is %s.\n" % self.returnPoints())
                # print(winningCardName)
                self.PlayTurn()

            self.askForReplay()


game = Game()
game.playGame()


# stuff i used for testing is below

'''
game.startGame()
print([card.name for card in game.deck.returnDeckofCards()])
print("\n" + str(game.deck.returnNumberofCards())+"\n\n\n")
game.deck.removeCard(game.deck.returnChosenCardfromPos(game.deck.returnNumberofCards() - 1).returnName())

game.deck.removeCard(game.deck.returnChosenCardfromPos(game.deck.returnNumberofCards() - 1).returnName())
game.changeDeck(game.defaultDeck)


print([card.name for card in game.deck.returnDeckofCards()])
print("\n" + str(game.deck.returnNumberofCards())+"\n\n\n")



'''


'''
deck = Deck()
print([card.name for card in deck.deckCards])
print("\ndeck initizalized\n")
deck.ShuffleDeck()
print([card.name for card in deck.deckCards])
print("\ndeck shuffled\n")
print(deck.returnChosenCardfromPos(51).returnName())

name = input("whatfdsaSdsfdsafadsfads?\n")
print(name)
'''

"""
if response == "Y":

elif response == "N":

else:
    print("Please respond with either \"Y\" or \"N\".")
"""
