from flask_mongoengine import MongoEngine

db = MongoEngine()


class User(db.Document):

	name = db.StringField(max_length= 300, required=True)
	wins = db.IntField(required = True)
	losses = db.IntField(required = True)
	
	meta = {
        'collection': 'player_names', # collection name
        'ordering': ['names'], # default ordering
        'auto_create_index': False, # MongoEngine will not create index
        }