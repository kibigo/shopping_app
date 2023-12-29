from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, User, Commodity, Review, Order, Payment
from flask_cors import CORS
from flask_session import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
app.config['SQLALCHEMY_TRACK_MODDIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['SESSION_TYPE'] = 'sqlalchemy'
app.json.compact = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)
app.config['SESSION_SQLALCHEMY'] = db

Session(app)
api = Api(app)
