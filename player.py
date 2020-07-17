from cards import Pile
class Player:
	def __init__(self, cards):
		self.cards = cards
		self.firstPlayer = False
		self.piles = [Pile(1), Pile(2), Pile(3), Pile(4), Pile(5)]
		self.authorized = False

	def getCards():
		return self.cards