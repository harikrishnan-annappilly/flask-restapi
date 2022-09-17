import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from .db import db

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))

app.secret_key = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db.init_app(app)

@app.route('/')
def index():
    return 'Home page revision 3'

api = Api(app)
jwt = JWTManager(app)

from app.resources.user import UserResource, UsersResource, LoginResource, RefreshLoginResource
from app.resources.item import ItemResource, ItemsResource
from app.resources.store import StoreResource, StoresResource
api.add_resource(UsersResource, '/users')
api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
api.add_resource(RefreshLoginResource, '/refresh')
api.add_resource(ItemsResource, '/items')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(StoresResource, '/stores')
api.add_resource(StoreResource, '/store/<string:name>')

@app.before_first_request
def create_all():
    db.create_all()
