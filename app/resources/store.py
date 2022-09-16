from flask_restful import Resource, reqparse

from app.models.store import StoreModel

_store_parser = reqparse.RequestParser()
_store_parser.add_argument('location', required=True, help='mandatory - hari')

class StoreResource(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store is None:
            return {
                'msg': f'store {name} not found'
            }, 404
        return store.json()

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {
                'msg': f'store name {name} already present'
            }, 400
        payload = _store_parser.parse_args()
        location = payload.get('location')
        store = StoreModel(name=name, location=location)
        store.save()
        return store.json(), 201

    def put(self, name):
        response_code = 500
        payload = _store_parser.parse_args()
        location = payload.get('location')
        store = StoreModel.find_by_name(name)
        if store:
            store.location = location
            response_code = 202
        else:
            store = StoreModel(name=name, location=location)
            response_code = 201
        store.save()
        return store.json(), response_code

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        response_code = 200
        if store:
            store.delete()
            response_code = 202
        return {
            'msg': f'store {name} deleted'
        }, response_code

class StoresResource(Resource):
    def get(self):
        return [store.json() for store in StoreModel.find_all()]
