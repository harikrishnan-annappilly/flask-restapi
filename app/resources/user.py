from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
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

class LoginResource(Resource):
    def post(self):
        payload = _user_parser.parse_args()
        username = payload.get('username')
        password = payload.get('password')
        user = UserModel.find_by_username(username)
        if user:
            if user.password == password:
                access_token = create_access_token(identity=username, fresh=True)
                refresh_token = create_refresh_token(identity=username)
                return {
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }
            return {
                'msg': 'password not match'
            }, 401
        return {
            'msg': f'user {username} not found'
        }, 400

class RefreshLoginResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity, fresh=False)
        return {
            'access_token': access_token,
        }
