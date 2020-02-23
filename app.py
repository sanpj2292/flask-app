from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.item import Item, ItemList
from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.store import Store, StoreList
from blacklist import BLACKLIST

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Flask modification tracker of SQLAlchemy is disabled not SQLAlchemy's Own Modification Tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Help in propagating the exceptions thrown
# by Extended Apps in Flask(Otherwise it will only throw 500 Error which is difficult
# to debug)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# A Secure Key
app.secret_key = 'SanPJ'
api = Api(app)

jwt = JWTManager(app=app)


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The Token has expired',
        'error': 'token_required'
    }), 401


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.invalid_token_loader
def invalid_token_callback(err):
    return jsonify({
        'description': 'Signature verification failed',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(err):
    return jsonify({
        'description': 'Request doesn\'t contain access token',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'Token is not fresh',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'Token has been revoked',
        'error': 'token_revoked'
    }), 401


api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(ItemList, '/item')
api.add_resource(StoreList, '/store')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')

if __name__ == '__main__':
    db.init_app(app=app)
    app.run(port=5000, debug=True)
