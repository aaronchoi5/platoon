import random
import cards
import winlossstate

class Player:
	def __init__(self, cards):
		self.cards = cards
		self.firstPlayer = False
		self.piles = [Pile(1), Pile(2), Pile(3), Pile(4), Pile(5)]
		self.authorized = False

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

			fightsWonA = 0
			fightsWonB = 0
			for trickNum in range(5):
				if turn % 2 == 0:
					playerA.authorized = True
					playerB.authorized = False
					#wait for player A's fight
					#playerA fights FE provides pileid for both fightsWinA +=1 if WIN or fightsWinB += 1 if LOSS or nothing if DRAW
				else:
					#playerB fights fightsWinB +=1 if WIN or fightsWinA += 1 if LOSS or nothing if DRAW
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


		#@app.route('/page/<username>')
		def assignCardsToPiles(piles):
			#post request most likely id part of route?
			if True:
				for i in range(5):
					self.playerA.piles[i].cards = piles[i]
				self.playerA.cards = []
			else:
				for i in range(5):
					self.playerB.piles[i].cards = piles[i]
				self.playerB.cards = []

			#return true
		def fight(pileA, pileB):
			#TODO do i pass in pile id's?
			#TODO check if player is authorized?

			#check for specials in pile A and pileB 
			#13 should be wizard, 12 should be king, 11 should be Queen, 10 = Jack, 9 = 10, ...,  0 = ace
			#resolve wizard wizard swaps piles
			if 13 in pileA and 13 in pileB:
				pass
			elif 13 in pileA:
				pileA, pileB = pileB, pileA

			elif 13 in pileB:
				pileA, pileB = pileB, pileA
			#king autowins unless facing an ace
			if 12 in pileA and 12 in pileB:
				return self.computeWinnerBasedOnCards(pileA, pileB)
			if 12 in PileB:
				if 0 in PileA:
					return winlossstate.WIN
			if 12 in pileA:
				if 0 in PileB:
					return winlossstate.LOSS
			if 0 in pileA and 0 in pileB:
				return self.computeWinnerBasedOnCards(pileA, pileB)
			#if ace in one or the other it loses
			if 0 in pileA:
				return winlossstate.LOSS
			if 0 in pileB:
				return winlossstate.WIN
			return self.computeWinnerBasedOnCards(pileA, pileB)

		def computeWinnerBasedOnCards(pileA, pileB):
			sumA = 0
			sumB = 0
			for a in pileA:
				if a != 13:
					sumA += a
			for b in pileB:
				if b != 13:
					sumB += b
			if a > b:
				return winlossstate.WIN
			elif a < b:
				return winlossstate.LOSS
			else:
				return winlossstate.DRAW


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