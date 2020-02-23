from flask_jwt_extended import (create_access_token, create_refresh_token,
                                jwt_refresh_token_required, get_jwt_identity, jwt_required, get_raw_jwt)
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.user import UserModel

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help='This field cannot be blank')
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help='This field cannot be blank')


class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.findByUsername(data['username']) is not None:
            return {'message': f'Username {data["username"]} already exists'}
        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'User created successfully'}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.findById(user_id)
        if user is None:
            return {'message': f'No user with user_id {user_id} is available'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.findById(user_id)
        if user is None:
            return {'message': f'No user with user_id {user_id} is available'}, 404
        user.delete()
        return {'message': f'User with user_id \'{user_id}\' deleted successfully'}


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.findByUsername(data['username'])
        # Access Token& Refresh Token Creation
        # this is what authenticate func used to do in security.py used to do
        if user and safe_str_cmp(data['password'], user.password):
            # This is what identity func is used for in security.py file
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        return {'message': 'Invalid User credentials'}


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'User successfully Logged out'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id, fresh=False)
        return {'access_token': new_token}, 200
