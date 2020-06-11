from flask import Flask, render_template
from models import db, User

# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)

## include db name in URI; _HOST entry overwrites all others
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/examples'

db.init_app(app)

@app.route("/login", methods=["GET" , "POST"])
def index():
	#fe sends username and password check those against db
	#redirect/send ok if valid else prompt them to reenter
	#have some kind of a lobby screen
	return ''

@app.route("/set")
def setAll():
	m = User.objects(name="test")
	m.update(set__wins=100)
	return ''

@app.route("start")
def startGame():
	#maybe use uuid as part of route?
	d = Deck()
	d.shuffle()
	pA = Player(d.cards[:10])
	pA = {
	"cards" = d.cards[:10],
	"firstPlayer" = False,
	"piles" = []
	"authorized" = False
	}
	pB = {
	"cards" = d.cards[10:20],
	"firstPlayer" = False,
	"piles" = []
	"authorized" = False
	}
	pB = Player(d.cards[10:20])
	rem = d[20:]
	g = Game(gameID= 0, remDeck = rem, playerA = pA, playerB = pB, roundsLeft = 5, trickNum = 0)

@app.route("resetDeck/<gameId>/<player>")
def resetDeck():
	g  = Game.objects(gameID= 0)
	roundsLeft = g.roundsleft
	if roundsLeft >=0:
		d = Deck()
		d.shuffle()
		pA = Player(d.cards[:10])
		pB = Player(d.cards[10:20])
		rem = d[20:]
		g = Game.objects(gameId = gameId).update(remDeck = rem, playerA = pA, playerB = pB, roundsleft = roundsleft-1, trickNum = 0)

@app.route("/<gameId>/assign/<player>")
def assignCards(piles):
	#piles will be a json array with cards in them
	g = Game.objects(gameId = gameId)

	if player == "a":
		for i in range(5):
			g.pA.piles[i] = piles[i]
	else:
		for i in range(5):
			g.pB.piles[i] = piles[i]

@app.route("/<gameId>/checkBothAssigned")
def pilesAreAssigned():
	g = Game.objects(gameId = gameId)
	playerA = g.playerA
	playerB = g.playerB
	for a in playerA.piles:
			if len(a.cards) < 1:
				return False
		for b in playerB.piles:
			if len(b.cards) < 1:
				return False
	return True

@app.route("/<gameId>/roundsLeft")
def roundsLeft():
	g = Game.objects(gameId = gameId)
	return g.rounds

@app.route("/<gameId>/startRound")
def startRound():
	g = Game.objects(gameId = gameId)

@app.route("/<gameId>/determineFirst")
def determineFirst():
	a, b = self.deck.cards[0].value, self.deck.cards[1].value
			while a == b:
				#TODO add logic to show cards as you see they are equal
				random.shuffle(self.deck.cards)
				a, b = self.deck.cards[0], self.deck.cards[1]
			
			if a.value > b.value:
				self.playerA.firstPlayer = True 
			else:
				self.playerB.firstPlayer = True
@app.route("/<gameId>/<player>/fight")
def fight(pileA, pileB):
	#use ids and assign appropriately
	g = Game.objects(gameId = gameId)
	pileA = g.objects(pA).piles[pileAId]
	pileB = g.objects(pB).piles[pileBId]

	if 13 in pileA and 13 in pileB:
			pass
		elif 13 in pileA:
			pileA, pileB = pileB, pileA

		elif 13 in pileB:
			pileA, pileB = pileB, pileA
		#king autowins unless facing an ace
		if 12 in pileA and 12 in pileB:
			return computeWinnerBasedOnCards(pileA, pileB)
		if 12 in PileB:
			if 0 in PileA:
				return winlossstate.WIN
		if 12 in pileA:
			if 0 in PileB:
				return winlossstate.LOSS
		if 0 in pileA and 0 in pileB:
			return computeWinnerBasedOnCards(pileA, pileB)
		#if ace in one or the other it loses
		if 0 in pileA:
			return winlossstate.LOSS
		if 0 in pileB:
			return winlossstate.WIN
		return computeWinnerBasedOnCards(pileA, pileB)

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