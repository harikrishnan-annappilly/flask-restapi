from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

from app.models.item import ItemModel
from app.models.store import StoreModel

_item_parser = reqparse.RequestParser()
_item_parser.add_argument('price', required=True, help='mandatory - hari')
_item_parser.add_argument('store')

class ItemResource(Resource):
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item is None:
            return {
                'msg': f'item {name} not found'
            }, 404
        return item.json()

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {
                'msg': f'item name {name} already present'
            }, 400
        payload = _item_parser.parse_args()
        price = payload.get('price')
        store = StoreModel.find_by_name(payload.get('store')) if payload.get('store') else None
        item = ItemModel(name=name, price=price, store=store)
        item.save()
        return item.json(), 201

    def put(self, name):
        response_code = 500
        payload = _item_parser.parse_args()
        price = payload.get('price')
        item = ItemModel.find_by_name(name)
        if item:
            item.price = price
            response_code = 202
        else:
            item = ItemModel(name=name, price=price)
            response_code = 201
        item.save()
        return item.json(), response_code

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        response_code = 200
        if item:
            item.delete()
            response_code = 202
        return {
            'msg': f'item {name} deleted'
        }, response_code

class ItemsResource(Resource):
    def get(self):
        return [item.json() for item in ItemModel.find_all()]
