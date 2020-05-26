import random
class Card:
    def __init__(self, value, color):
        self.value = value
        self.suit = color

class Deck:
	def __init__(self):
		self.cards = []
		colors = ['heart', 'spades']
		for c in colors:
			for i in range(14):
				self.cards.append(Card(i, c))

	def shuffle(self):
		random.shuffle(self.cards)

class Player:
	def __init__(self, cards):
		self.cards = cards
		self.firstPlayer = False
		self.pile1 = []
		self.pile2 = []
		self.pile3 = []
		self.pile4 = []
		self.pile5 = []
		#guid for security?

class Game:
	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.playerA = Player(self.deck.cards[:10])
		self.playerB = Player(self.deck.cards[10:20])
		self.deck.cards = self.deck.cards[20:]

	class Round:
		def determineFirst(self):
			a, b = self.deck.cards[0].value, self.deck.cards[1].value
			while a == b:
				#TODO add logic to show cards as you see they are equal
				random.shuffle(self.deck.cards)
				a, b = self.deck.cards[0], self.deck.cards[1]
			
			if a.value > b.value:
				self.playerA.firstPlayer = True 
			else:
				self.playerB.firstPlayer = True

		def assignCardsToPiles(pile1, pile2, pile3, pile4, pile5):
			#post request most likely id part of route?
			if True:
				self.playerA.pile1 = pile1
				self.playerA.pile2 = pile2
				self.playerA.pile3 = pile3
				self.playerA.pile4 = pile4
				self.playerA.pile5 = pile5
				self.playerA.cards = []
			else:
				self.playerB.pile1 = pile1
				self.playerB.pile2 = pile2
				self.playerB.pile3 = pile3
				self.playerB.pile4 = pile4
				self.playerB.pile5 = pile5
				self.playerB.cards = []
				
			#return true


		class Trick:
			def __init__(self):


		

g = Game()

a = g.playerA.cards
b = g.playerB.cards
remainer = g.deck.cards
for x in a:
	print(x.suit, x.value)
for y in b:
	print(y.suit, y.value)
for q in remainer:
	print(q.suit, q.value, "r")