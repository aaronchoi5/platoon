from cards import Pile
class Player:
	def __init__(self, cards, username, authorized):
		self.cards = cards
		self.piles = [Pile(1), Pile(2), Pile(3), Pile(4), Pile(5)]
		self.authorized = authorized
		self.name = username
		self.roundsWon = 0
		self.tricksWon = 0

	def getCards():
		return self.cards