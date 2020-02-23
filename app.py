from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.item import Item, ItemList
from resources.user import UserRegister
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Flask modification tracker of SQLAlchemy is disabled not SQLAlchemy's Own Modification Tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Help in propagating the exceptions thrown
# by Extended Apps in Flask(Otherwise it will only throw 500 Error which is difficult
# to debug)
app.config['PROPAGATE_EXCEPTIONS'] = True
# A Secure Key
app.secret_key = 'SanPJ'
api = Api(app)

jwt = JWT(app=app, authentication_handler=authenticate, identity_handler=identity)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(UserRegister, '/register')
api.add_resource(ItemList, '/item')
api.add_resource(StoreList, '/store')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')

if __name__ == '__main__':
    db.init_app(app=app)
    app.run(port=5000, debug=True)
