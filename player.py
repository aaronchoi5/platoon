from cards import Pile
class Player:
	def __init__(self, cards, username, authorized):
		self.cards = cards
		self.firstPlayer = False
		self.piles = [Pile(1), Pile(2), Pile(3), Pile(4), Pile(5)]
		self.authorized = authorized
		self.name = username

	def getCards():
		return self.cards