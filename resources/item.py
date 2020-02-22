from apps import reqparse, jwt_required, Resource
import sqlite3

from models.item import ItemModel


# API works with Resources
class Item(Resource):
    reqParser = reqparse.RequestParser()
    reqParser.add_argument('price', type=float, required=True, help='This field is required')
    reqParser.add_argument('store_id', type=int, required=True, help='Every item needs a Store ID')

    @jwt_required()
    def get(self, name):
        item = ItemModel.findByName(name)
        if item:
            return item.json()
        return {'message': 'Item doesn\'t exist'}, 404

    def post(self, name):
        if ItemModel.findByName(name):
            return {'message': f'Item with name {name} already exists'}, 400
        data = Item.reqParser.parse_args()
        insert_item = ItemModel(_id=None, name=name, price=data['price'], store_id=data['store_id'])
        try:
            insert_item.save_to_db()
        except:
            return {'message': 'An Error Occurred while inserting Data'}, 500
        return insert_item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.findByName(name)
        if item is None:
            return {'message': f'Item with name \'{name}\' doesn\'t exist'}
        item.delete()
        return {'message': f'Item with name \'{name}\' Deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.reqParser.parse_args()
        item = ItemModel.findByName(name)
        is_insert = item is None
        try:
            if is_insert:
                item = ItemModel(None, name=name, price=data['price'], store_id=data['store_id'])
            else:
                item.price = data['price']
            item.save_to_db()
        except:
            typeOfAction = 'Inserting' if is_insert else 'Updating'
            return {'message': f'An Error occurred while {typeOfAction} the item'}, 500
        return item.json()


class ItemList(Resource):
    def get(self):
        items = ItemModel.castToItems(ItemModel.query.all())
        return {'items': items}
