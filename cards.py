import random
import uuid
class Card:
    def __init__(self, value, color):
        self.value = value
        self.suit = color

class Deck:
	def __init__(self):
		self.cards = []
		colors = ['heart', 'spades']
		for c in colors:
			for i in range(15):
				self.cards.append(Card(i, c))

	def shuffle(self):
		random.shuffle(self.cards)
class Pile:
	def __init__(self, pileId):
		self.cards = []
		self.id = pileId