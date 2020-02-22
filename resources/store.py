from flask_restful import Resource, reqparse
from models.store import StoreModel

class Store(Resource):
    reqParser = reqparse.RequestParser()
    reqParser.add_argument('price', type=float, required=True, help='This field is required')
    reqParser.add_argument('store_id', type=int, required=True, help='Every item needs a Store ID')

    def get(self, name):
        store = StoreModel.findByName(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.findByName(name):
            return {'message': f'Store with name \'{name}\' already Exists'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.findByName(name)
        if store:
            store.delete(name)

        return {'message': f'Store has been with name \'{name}\' deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
    pass