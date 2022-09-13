from flask_restful import Resource, reqparse
from app.models.user import UserModel

_user_parser_username = reqparse.RequestParser()
_user_parser_username.add_argument('username', required=True, help='This is mandatory - hari')
_user_parser = _user_parser_username.copy()
_user_parser.add_argument('password', required=True, help='This is mandatory - hari')

class UserResource(Resource):

    def get(self):
        payload = _user_parser_username.parse_args()
        username = payload.get('username')
        user = UserModel.find_by_username(username)
        if user is None:
            return {
                'msg': f'user {username} not found'
            }, 404
        return user.json(), 200

    def post(self):
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')
        if UserModel.find_by_username(username):
            return {
                'msg': f'username {username} already taken'
            }, 400
        user = UserModel(username=username, password=password)
        user.save()
        return user.json(), 201

    def put(self):
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')
        user = UserModel.find_by_username(username)
        response_code = 500
        if user:
            user.password = password
            response_code = 202
        else:
            user = UserModel(username=username, password=password)
            response_code = 201
        user.save()
        return user.json(), response_code

    def delete(self):
        payload = _user_parser_username.parse_args()
        username = payload.get('username')
        user = UserModel.find_by_username(username)
        if user:
            user.delete()
        return {
            'msg': f'user {username} is deleted'
        }, 201

class UsersResource(Resource):
    def get(self):
        return [user.json() for user in UserModel.find_all()], 200
