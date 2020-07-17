from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):

	username = db.StringField(max_length= 300, required=True)
	wins = db.IntField(required = True)
	losses = db.IntField(required = True)
	password = db.StringField(required=True)
	
	meta = {
        'collection': 'player_names', # collection name
        'ordering': ['names'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }

class Game(db.Document):
	gameID = db.UUIDField()
	remDeck = db.BinaryField(required=True)
	playerADataField = db.BinaryField(required = True)#player could have user name as key?
	playerBDataField = db.BinaryField(required = True)
	roundsLeft = db.IntField(required = True)
	trickNum = db.IntField(required = True)

	meta = {
        'collection': 'games', # collection name
        'ordering': ['names'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }

class LookingForGame(db.Document):
	username = db.StringField(max_length= 300, required=True)
	
	meta = {
        'collection': 'LookingForGame', # collection name
        'ordering': ['username'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }