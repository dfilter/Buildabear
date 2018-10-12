from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt)
from passlib.hash import pbkdf2_sha256

from app.utils import Queries
from app import jwt


parser = reqparse.RequestParser()
parser.add_argument(
    'username', help='This field cannot be blank', required=True)
parser.add_argument(
    'password', help='This field cannot be blank', required=True)
parser.add_argument(
    'email', help='This field cannot be blank', required=True)


@jwt.token_in_blacklist_loader
def is_token_in_blacklist_loader(decrypted_token):
    return bool(Queries.select_token(decrypted_token['token']))


class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        try:
            if Queries.select_user(username=data['username'], email=data['email']):
                return {
                    'message': 'A user with the username {0} or email {1} already exists.'.
                    format(data['username'], data['email'])
                }
            pasword_hash = pbkdf2_sha256.hash(data['password'])
            Queries.insert_user(
                data['username'], data['email'], pasword_hash)
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except:
            return {'message': 'Something went wrong!'}, 500


class UserLogin(Resource):

    def post(self):
        data = parser.parse_args()
        try:
            user = Queries.select_user(
                username=data['username'], email=data['email'])
            if not user:
                return {
                    'message': 'A user with the username {0} or email {1} does not exist.'.format(data['username'], data['email'])
                }
            if pbkdf2_sha256.verify(data['password'], user['password_hash']):
                access_token = create_access_token(identity=data['username'])
                refresh_token = create_refresh_token(identity=data['username'])
                return {
                    'message': 'Current user: {0} password: {1}'.format(user['username'], user['password_hash']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            else:
                return {'message': 'Login username/email and password pair are incorrect.'}
        except:
            return {'message': 'Something went wrong!'}, 500


class UserLogoutAccess(Resource):

    @jwt_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            Queries.insert_token(token)
            return {'message': 'Access token is no longer valid.'}
        except:
            return {'message': 'Something went wrong!'}, 500


class UserLogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            Queries.insert_token(token)
            return {'message': 'Refresh token is no longer valid.'}
        except:
            return {'message': 'Something went wrong!'}, 500


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class SecretResource(Resource):

    @jwt_required
    def get(self):
        return {'answer': 42}
