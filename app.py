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
import json
from winlossstate import winlossstate

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

clients = {}

@socketio.on('connect')
def test_connect():
	send('after connect')

@socketio.on('disconnect')
def handle_disconnect():
    send('Client disconnected')
    clients.pop(request.sid)

@socketio.on('user session registration')
def register_session(username):
	clients[username] = request.sid

@socketio.on('host game')
def hostGames(username):
	gameQueue = LookingForGame(username = username)
	gameQueue.save()
	#emit looking for game users event to update lobby
	updateLobby()
	print('host games works')

@socketio.on('user challenge')
def challenge(payload):
	recipient_session_id = clients[payload['challengee_username']]
	print(payload['challenger_username'] + ' vs ' + payload['challengee_username'])
	socketio.emit('challenge', payload['challenger_username'], room=recipient_session_id)

@socketio.on('active users')
def handle_users():
    users = User.objects()
    players = [user.username for user in users] 
    emit( players)

@socketio.on('get username')
def get_user_name():
	for client in clients:
		sId = clients[client]
		if sId == request.sid:
			emit('challenge', room=sId)

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
	else:
		return "Wrong username/password", 403

@app.route("/register", methods=["POST"])
def register():
	#fe sends username and password to be registered in db
	request_json = request.get_json()
	username = request_json.get('username')
	password = request_json.get('password')
	encryptedPassword = returnEncryptedText(password)
	#if user exists return something that says they exist
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

@socketio.on('looking for game users')
def returnPlayersLookingForGames():
	updateLobby()

def updateLobby():
	gameQueue = LookingForGame.objects()
	players = [game.username for game in gameQueue] 
	emit('looking for game users', players)

@socketio.on('set up game')
def setUpGame(payload):
	playerAName = payload['challengee_username']
	playerBName = payload['challenger_username']
	deck = Deck()
	deck.shuffle()
	authorized = True if random.randint(0,1) == 0 else False
	playerA = Player(deck.cards[:10], playerAName, authorized)
	playerB = Player(deck.cards[10:20], playerBName, not authorized)
	remainingCards = deck.cards[20:]
	playerAbytes = pickle.dumps(playerA)
	playerBbytes = pickle.dumps(playerB)
	remainingCardsBytes = pickle.dumps(remainingCards)
	gameId = uuid.uuid4()

	game = Game(gameID= gameId, remDeck = Binary(remainingCardsBytes), playerADataField = Binary(playerAbytes), playerBDataField = Binary(playerBbytes), roundsLeft = 5, trickNum = 0)
	game.save()
	recipient_session_idA = clients[playerAName]
	recipient_session_idB = clients[playerBName]

	emit('go to game view', str(gameId), room=recipient_session_idA)
	emit('go to game view', str(gameId), room=recipient_session_idB)#maybe store this in store for use in frontend

@socketio.on('get player cards')
def getCards(payload):
	username = payload['username']
	gameId = payload['gameId']
	games = Game.objects(gameID = gameId)

	dataA = [game.playerADataField for game in games]
	binDataA = dataA[0]

	dataB = [game.playerBDataField for game in games]
	binDataB = dataB[0]

	playerA = pickle.loads(binDataA)
	playerB = pickle.loads(binDataB)
	recipient_session_id = clients[username]

	if username == playerA.name:
		playerACards = playerA.cards
		playerACardsList = []
		for card in playerACards:
			jsonStrA = json.dumps(card.__dict__)
			playerACardsList.append(jsonStrA)
		emit('assign cards', playerACardsList, room = recipient_session_id)
		print('playerA emitted')
	elif username == playerB.name:
		playerBCards = playerB.cards
		playerBCardsList = []
		for card in playerBCards:
			jsonStrB = json.dumps(card.__dict__)
			playerBCardsList.append(jsonStrB)
		emit('assign cards', playerBCardsList, room = recipient_session_id)
		print('playerB emitted')
	else:
		print('Something is up.')

	print('it ran')
	print('username: ' + username + 'playerA: ' + playerA.name + 'playerB: ' + playerB.name)

@socketio.on('assign piles')
def assignPiles(payload):
	username = payload['username']
	gameId = payload['gameId']
	games = Game.objects(gameID = gameId)
	game = games.get(gameID = gameId)

#refactor this mess later
	dataA = [game.playerADataField for game in games]
	binDataA = dataA[0]

	dataB = [game.playerBDataField for game in games]
	binDataB = dataB[0]

	playerA = pickle.loads(binDataA)
	playerB = pickle.loads(binDataB)
	recipient_session_id = clients[username]
	piles = payload['piles']

	if username == playerA.name:
		for i in range(5):
			playerA.piles[i].cards = piles[i]

		game.playerADataField = Binary(pickle.dumps(playerA))
		game.save()
		if pilesReady(playerB.piles):
			emit('Both Ready', {"authorized": playerA.authorized, "piles": [len(playerB.piles[0].cards), len(playerB.piles[1].cards), len(playerB.piles[2].cards), len(playerB.piles[3].cards), len(playerB.piles[4].cards)]}, room = recipient_session_id)
			opponent_session_id = clients[playerB.name]
			emit('Both Ready', {"authorized": playerB.authorized, "piles": [len(playerA.piles[0].cards), len(playerA.piles[1].cards), len(playerA.piles[2].cards), len(playerA.piles[3].cards), len(playerA.piles[4].cards)]}, room = opponent_session_id)
			
		else:
			emit('Waiting', room = recipient_session_id)

		#TODO maybe run method that'll emit certain event that'll trigger if both have assigned piles else emit event that'll say to wait
		print('playerA emitted') 
	elif username == playerB.name:
		for i in range(5):
			playerB.piles[i].cards = piles[i] 

		game.playerBDataField = Binary(pickle.dumps(playerB))
		game.save()

		if pilesReady(playerA.piles):
			emit('Both Ready',{"authorized": playerB.authorized, "piles": [len(playerA.piles[0].cards), len(playerA.piles[1].cards), len(playerA.piles[2].cards), len(playerA.piles[3].cards), len(playerA.piles[4].cards)]}, room = recipient_session_id)
			opponent_session_id = clients[playerA.name]
			emit('Both Ready',{"authorized": playerA.authorized, "piles": [len(playerB.piles[0].cards), len(playerB.piles[1].cards), len(playerB.piles[2].cards), len(playerB.piles[3].cards), len(playerB.piles[4].cards)]}, room = opponent_session_id)
			
		else:
			emit('Waiting', room = recipient_session_id)

		emit('todo', room = recipient_session_id)
		print('playerB emitted')
	else:
		print('Something is up.')

@socketio.on('fight')
def startFight(payload):
	username = payload['username']
	battlingPiles = payload['battlingPiles']
	gameId = payload['gameId']
	recipient_session_id = clients[username]
	games = Game.objects(gameID = gameId)
	game = games.get(gameID = gameId)
#refactor this mess later
	binDataA = game.playerADataField
	binDataB = game.playerBDataField

	playerA = pickle.loads(binDataA)
	playerB = pickle.loads(binDataB)

	if username == playerA.name:
		pileAId = battlingPiles[0]
		pileBId = battlingPiles[1]
		opponent_session_id = clients[playerB.name]
		pileA = []
		for card in playerA.piles[pileAId].cards:
			pileA.append(card['value'])
		pileB = []
		for card in playerB.piles[pileBId].cards:
			pileB.append(card['value'])

		winlossA = fight(pileA, pileB)
		if game.roundsLeft == 0 and game.trickNum == 4:
			if winlossA == winlossstate.WIN:
					playerA.tricksWon += 1
			elif winlossA == winlossstate.LOSS:
					playerB.tricksWon += 1

			if playerA.roundsWon < playerB.roundsWon:
				emit('game over', "lost", room = recipient_session_id)
				emit('game over', "won", room = opponent_session_id)
			elif playerA.roundsWon > playerB.roundsWon:
				emit('game over', "won", room = recipient_session_id)
				emit('game over', "lost", room = opponent_session_id)
			else:
				emit('game over', "drew", room = recipient_session_id)
				emit('game over', "drew", room = opponent_session_id)
		else:
			if game.trickNum == 4:
				resetDeck(game, playerA, playerB)
				resetHandling(playerA, playerB, recipient_session_id, opponent_session_id, winlossA)
			else:
				fightHandling(game, playerA, playerB, pileAId, pileBId, recipient_session_id, opponent_session_id, winlossA)
	else:
		pileAId = battlingPiles[1]
		pileBId = battlingPiles[0]
		opponent_session_id = clients[playerA.name]
		pileA = []
		for card in playerA.piles[pileAId].cards:
			pileA.append(card['value'])
		pileB = []
		for card in playerB.piles[pileBId].cards:
			pileB.append(card['value'])
		winlossB = fight(pileA, pileB)
		playerA.piles[pileAId].cards = []
		playerB.piles[pileBId].cards = []

		if game.roundsLeft == 0 and game.trickNum == 4:
			if winlossB == winlossstate.WIN:
					playerB.tricksWon += 1
			elif winlossB == winlossstate.LOSS:
					playerB.tricksWon += 1
			if playerA.roundsWon < playerB.roundsWon:
				emit('game over', "lost", room = recipient_session_id)
				emit('game over', "won", room = opponent_session_id)
			elif playerA.roundsWon > playerB.roundsWon:
				emit('game over', "won", room = recipient_session_id)
				emit('game over', "lost", room = opponent_session_id)
			else:
				emit('game over', "drew", room = recipient_session_id)
				emit('game over', "drew", room = opponent_session_id)
		else:
			if game.trickNum == 4:
				resetDeck(game, playerA, playerB)
				resetHandling(playerB, playerA, recipient_session_id, opponent_session_id, winlossB)
			else:
				fightHandling(game, playerB, playerA, pileBId, pileAId, recipient_session_id, opponent_session_id, winlossB)
	
	playerA.authorized = not playerA.authorized
	playerB.authorized = not playerB.authorized
	game.playerADataField = Binary(pickle.dumps(playerA))
	game.playerBDataField = Binary(pickle.dumps(playerB))
	game.save()
#wip think about using this in player b's case too to reduce lines of code?
def resetHandling(player1, player2, recipient_session_id, opponent_session_id, winlossA):
	player1CardsList = []
	for card in player1.cards:
		jsonStrA = json.dumps(card.__dict__)
		player1CardsList.append(jsonStrA)
	player2CardsList = []
	for card in player2.cards:
		jsonStrB = json.dumps(card.__dict__)
		player2CardsList.append(jsonStrB)
	if winlossA == winlossstate.WIN:
		player1.tricksWon += 1
		emit('win reset', {"authorized": not player1.authorized, "newCards": player1CardsList}, room = recipient_session_id)
		emit('loss reset', {"authorized": not player2.authorized, "newCards": player2CardsList}, room = opponent_session_id)
	elif winlossA == winlossstate.LOSS:
		player2.tricksWon += 1
		emit('win reset', {"authorized": not player2.authorized, "newCards": player2CardsList}, room = opponent_session_id)
		emit('loss reset', {"authorized": not player1.authorized, "newCards": player1CardsList}, room = recipient_session_id)
	else:
		emit('draw reset', {"authorized": not player1.authorized, "newCards": player1CardsList}, room = recipient_session_id)
		emit('draw reset', {"authorized": not player2.authorized, "newCards": player2CardsList}, room = opponent_session_id)
	if player1.tricksWon > player2.tricksWon:
		player1.roundsWon += 1
	elif player2.tricksWon > player1.tricksWon:
		player2.roundsWon += 1

def fightHandling(game, player1, player2, pile1Id, pile2Id, recipient_session_id, opponent_session_id, winlossA):
	game.trickNum += 1
	game.save()
	player1.piles[pile1Id].cards = []
	player2.piles[pile2Id].cards = []
	if winlossA == winlossstate.WIN:
		player1.tricksWon += 1
		emit('win', {"authorized": not player1.authorized, "pilesA": [player1.piles[0].cards, player1.piles[1].cards, player1.piles[2].cards, player1.piles[3].cards, player1.piles[4].cards], "pilesB": [len(player2.piles[0].cards), len(player2.piles[1].cards), len(player2.piles[2].cards),len(player2.piles[3].cards),len(player2.piles[4].cards)]}, room = recipient_session_id)
		emit('loss', {"authorized": not player2.authorized, "pilesA": [player2.piles[0].cards, player2.piles[1].cards, player2.piles[2].cards, player2.piles[3].cards, player2.piles[4].cards], "pilesB": [len(player1.piles[0].cards), len(player1.piles[1].cards), len(player1.piles[2].cards),len(player1.piles[3].cards),len(player1.piles[4].cards)]}, room  = opponent_session_id)
	elif winlossA == winlossstate.LOSS:
		player2.tricksWon += 1
		emit('win', {"authorized": not player2.authorized, "pilesA": [player2.piles[0].cards, player2.piles[1].cards, player2.piles[2].cards, player2.piles[3].cards, player2.piles[4].cards], "pilesB": [len(player1.piles[0].cards), len(player1.piles[1].cards), len(player1.piles[2].cards),len(player1.piles[3].cards),len(player1.piles[4].cards)]}, room = opponent_session_id)
		emit('loss', {"authorized": not player1.authorized, "pilesA": [player1.piles[0].cards, player1.piles[1].cards, player1.piles[2].cards, player1.piles[3].cards, player1.piles[4].cards], "pilesB": [len(player2.piles[0].cards), len(player2.piles[1].cards), len(player2.piles[2].cards),len(player2.piles[3].cards),len(player2.piles[4].cards)]}, room = recipient_session_id)
	else:
		emit('draw', {"authorized": not player1.authorized, "pilesA": [player1.piles[0].cards, player1.piles[1].cards, player1.piles[2].cards, player1.piles[3].cards, player1.piles[4].cards], "pilesB": [len(player2.piles[0].cards), len(player2.piles[1].cards), len(player2.piles[2].cards),len(player2.piles[3].cards),len(player2.piles[4].cards)]}, room = recipient_session_id)
		emit('draw', {"authorized": not player2.authorized, "pilesA": [player2.piles[0].cards, player2.piles[1].cards, player2.piles[2].cards, player2.piles[3].cards, player2.piles[4].cards], "pilesB": [len(player1.piles[0].cards), len(player1.piles[1].cards), len(player1.piles[2].cards),len(player1.piles[3].cards),len(player1.piles[4].cards)]}, room = opponent_session_id)

def fight(pileA, pileB):
	if 13 in pileA and 13 in pileB:
		pass
	elif 13 in pileA:
		pileA, pileB = pileB, pileA
	elif 13 in pileB:
		pileA, pileB = pileB, pileA
	#king autowins unless facing an ace
	if 12 in pileA and 12 in pileB:
		return computeWinnerBasedOnCards(pileA, pileB)
	if 12 in pileB:
		if 0 in pileA:
			return winlossstate.WIN
		else:
			return winlossstate.LOSS
	if 12 in pileA:
		if 0 in pileB:
			return winlossstate.LOSS
		else:
			return winlossstate.WIN
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

def pilesReady(piles):
	for i in range(len(piles)):
		if len(piles[i].cards) < 1:
			return False
	return True

def resetDeck(game, player1, player2):
	deck = Deck()
	deck.shuffle()
	player1.authorized = not player1.authorized
	player2.authorized = not player2.authorized
	player1.cards = deck.cards[:10]
	player2.cards = deck.cards[10:20]
	remainingCards = deck.cards[20:]
	player1bytes = pickle.dumps(player1)
	player2bytes = pickle.dumps(player2)
	remainingCardsBytes = pickle.dumps(remainingCards)
	game.playerADataField = player1bytes
	game.playerBDataField = player2bytes
	game.remDeck = remainingCardsBytes
	game.roundsLeft -= 1
	game.trickNum = 0
	game.save()



if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0')