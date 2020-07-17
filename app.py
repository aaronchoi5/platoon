from flask import Flask, render_template, request, redirect
from models import db, User, Game, LookingForGame
from cards import *
from bson.binary import Binary
from flask_cors import CORS
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from flask_socketio import SocketIO, send, emit
import uuid
from player import Player
import pickle
import random
import os
import sys
import eventlet


# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")
#socketio.init_app(app, cors_allowed_origins="*")

## include db name in URI; _HOST entry overwrites all others
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/examples'

db.init_app(app)
CORS(app, support_credentials=True)

@socketio.on('connect')
def test_connect():
	send('after connect')

@socketio.on('active users')
def handle_users():
    users = User.objects()
    players = [user.username for user in users] 
    emit( players)
    
@app.route("/login", methods=["POST"])
def login():
	#fe sends username and password check those against db
	#redirect/send ok if valid else prompt them to reenter
	#have some kind of a lobby screen
	request_json = request.get_json()
	uname = request_json.get('username')
	password = request_json.get('password')
	user = User.objects(username = uname)
	
	passW = user[0].password
	if checkEncryptedText(passW).rstrip() == password:
		return ''

	return ''

@app.route("/register", methods=["POST"])
def register():
	#fe sends username and password to be registered in db
	request_json = request.get_json()
	username = request_json.get('username')
	password = request_json.get('password')
	encryptedPassword = returnEncryptedText(password)
	user = User(username = username, wins = 0, losses = 0, password = encryptedPassword)
	user.save()
	print(encryptedPassword)
	return ''

def returnEncryptedText(text):
	paddedtext = text
	with open("./data/key.txt") as kf:
		keytext = kf.read()
		#padding the text because the text has to be divisible by the block size which 128 bits or 16 bytes in AES
	while((len(paddedtext) % 16) != 0):
		paddedtext += " "
	with open("./data/iv.txt") as ivf:
		ivtext = ivf.read()

	iv = bytes([int(b,16) for b in ivtext.split("0x")[1:]])
	key = bytes([int(b,16) for b in keytext.split("0x")[1:]])

	backend = default_backend()
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
	encryptor = cipher.encryptor()
	ciphertext = encryptor.update(paddedtext.encode(encoding='UTF-8')) + encryptor.finalize()
	#writes the ciphertext to a file
	return "".join(["0x{0}".format(format(byte,"02x")) for byte in ciphertext])

def checkEncryptedText(encryptedText):
	with open("./data/key.txt") as kf:
		keytext = kf.read()
	with open("./data/iv.txt") as ivf:
		ivtext = ivf.read()
	backend = default_backend()
	key = bytes([int(b,16) for b in keytext.split("0x")[1:]])
	iv = bytes([int(b,16) for b in ivtext.split("0x")[1:]])
	cipherbytes = bytes([int(b,16) for b in encryptedText.split("0x")[1:]])
	cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
	decryptor = cipher.decryptor()
	decryptedstr = decryptor.update(cipherbytes) + decryptor.finalize()

	#turns the byte string back into a hexadecimal string and translates that to readable text 
	result =  "".join(["{0}".format(format(byte,"02x")) for byte in decryptedstr])
	translatedResult = bytearray.fromhex(result).decode()
	return translatedResult

@app.route("/lookForGame", methods=["POST"])
def postGames():
	request_json = request.get_json()
	username = request_json.get('username')
	gameQueue = LookingForGame(username = username)
	gameQueue.save()
	#emit looking for game users event to update lobby
	updateLobby()
	return ''

@socketio.on('looking for game users')
def returnPlayersLookingForGames():
	updateLobby()

def updateLobby():
	gameQueue = LookingForGame.objects()
	players = [game.username for game in gameQueue] 
	emit('looking for game users', players)

@app.route("/test")
def xxxx():
	socketio.emit('looking for game users', ["sssss","a", "ree"])
	return ''
@app.route("/start")
def startGame():
	#maybe use uuid as part of route?
	deck = Deck()
	deck.shuffle()
	playerA = Player(deck.cards[:10])
	playerB = Player(deck.cards[10:20])
	remainingCards = deck.cards[20:]
	playerAbytes = pickle.dumps(playerA)
	playerBbytes = pickle.dumps(playerB)
	remainingCardsBytes = pickle.dumps(remainingCards)

	game = Game(gameID= uuid.uuid4(), remDeck = Binary(remainingCardsBytes), playerADataField = Binary(playerAbytes), playerBDataField = Binary(playerBbytes), roundsLeft = 5, trickNum = 0)
	game.save()
	return ''

@app.route("/deserialize/<gameid>")
def deserialize():
	games = Game.objects(roundsLeft = 5)
	rem = [game.remDeck for game in games]
	playerA = [game.playerADataField for game in games]
	binData = rem[0]
	binDataA = playerA[0]
	remaining = pickle.loads(binData)
	for r in remaining:
		print("Remaining Cards: ",r.suit, r.value)

	playerADeserialized = pickle.loads(binDataA)
	print("playerA: ", playerADeserialized.cards[0].suit, playerADeserialized.cards[0].value)
	
	print(remaining)
	return ""

@app.route("/resetDeck/<gameId>/<player>")
def resetDeck():
	g  = Game.objects(gameId = gameId)
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

if __name__ == '__main__':
    socketio.run(app)