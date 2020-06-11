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
	#redirect if valid else prompt them to reenter
	return ''

@app.route("/set")
def setAll():
	m = User.objects(name="test")
	m.update(set__wins=100)
	return ''

