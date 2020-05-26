import random
import cards

class Player:
	def __init__(self, cards):
		self.cards = cards
		self.firstPlayer = False
		self.pile1 = Pile()
		self.pile2 = Pile()
		self.pile3 = Pile()
		self.pile4 = Pile()
		self.pile5 = Pile()
		#guid for security?
	def getCards():
		return self.cards

class Game:
	def __init__(self):
		self.deck = Deck()
		self.deck.shuffle()
		self.playerA = Player(self.deck.cards[:10])
		self.playerB = Player(self.deck.cards[10:20])
		self.deck.cards = self.deck.cards[20:]

	def start(numOfRounds):
		for i in numOfRounds:
			self.deck = Deck()
			self.deck.shuffle()
			self.playerA = Player(self.deck.cards[:10])
			self.playerB = Player(self.deck.cards[10:20])
			self.deck.cards = self.deck.cards[20:]

			r = Round()
			#get requests to get player's cards so we can display them on screen
			r.assignCardsToPiles()

			r.determineFirst()
			turn = 0 if self.playerA.firstPlayer else 1

			for trickNum in range(5):
				if turn % 2 == 0:
					#playerA fights FE provides guid for both
				else:
					#playerB fights
				turn += 1

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
				self.playerA.pile1.cards = pile1
				self.playerA.pile2.cards = pile2
				self.playerA.pile3.cards = pile3
				self.playerA.pile4.cards = pile4
				self.playerA.pile5.cards = pile5
				self.playerA.cards = []
			else:
				self.playerB.pile1.cards = pile1
				self.playerB.pile2.cards = pile2
				self.playerB.pile3.cards = pile3
				self.playerB.pile4.cards = pile4
				self.playerB.pile5.cards = pile5
				self.playerB.cards = []

			#return true
		def fight(pileA, pileB):
			#TODO do i pass in pile id's?
			#check for specials in pile A and pileB 
			#13 should be wizard, 12 should be king, 11 should be Queen, 10 = Jack, 9 = 10, ...,  0 = ace
			#resolve wizard
			#if 13 in pileA:  pileA, pileB = pileB, pileA
			#if 13 in pileB:  pileA, pileB = pileB, pileA
			#if 12 in both check for higher values
			#if 12 in pileA: checkForAce if ace in PileB B wins vice versa
			#if 12 in pileB: as above
			#if ace in both check for higher values if none than it's a tie
			#if ace in one or the other it loses
			#total up cards in each pile and see which one is higher


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