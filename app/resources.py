from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt)
from passlib.hash import pbkdf2_sha256

from app.utils import Queries, DS3Queries
from app import jwt


parser = reqparse.RequestParser()
parser.add_argument(
    'password', help='This field cannot be blank')
parser.add_argument(
    'email', help='This field cannot be blank')
parser.add_argument(
    'username', help='This field cannot be blank')
parser.add_argument(
    'password', help='This field cannot be blank')
parser.add_argument(
    'user_id', help='This field cannot be blank')
parser.add_argument(
    'author_id', help='This field cannot be blank')
parser.add_argument(
    'subscription_id', help='This field cannot be blank')
parser.add_argument(
    'associated_id', help='This field cannot be blank')
parser.add_argument(
    'comment', help='This field cannot be blank')
parser.add_argument(
    'reply_id', help='This field cannot be blank')
parser.add_argument(
    'comment_id', help='This field cannot be blank')
parser.add_argument(
    'rating_id', help='This field cannot be blank')
parser.add_argument(
    'rate', help='This field cannot be blank')
parser.add_argument(
    'view', help='This field cannot be blank')
parser.add_argument(
    'game_id', help='This field cannot be blank')
parser.add_argument(
    'post_description', help='This field cannot be blank')
parser.add_argument(
    'post_text', help='This field cannot be blank')
parser.add_argument(
    'stats_dict', help='This field cannot be blank')    
parser.add_argument(
    'stat_allocation_id', help='This field cannot be blank')
parser.add_argument(
    'build_id', help='This field cannot be blank')
parser.add_argument(
    'tag_list', help='This field cannot be blank')
parser.add_argument(
    'item_list', help='This field cannot be blank')
parser.add_argument(
    'stat_description', help='This field cannot be blank')
parser.add_argument(
    'item_description', help='This field cannot be blank')
parser.add_argument(
    'hours', help='This field cannot be blank')
parser.add_argument(
    'order', help='This field cannot be blank')
parser.add_argument(
    'desending', help='This field cannot be blank')
parser.add_argument(
    'build_markup', help='This field cannot be blank')
parser.add_argument(
    'image_url', help='This field cannot be blank')
parser.add_argument(
    'post_id', help='This field cannot be blank')
parser.add_argument(
    'reply_id', help='This field cannot be blank')
parser.add_argument(
    'build_description', help='This field cannot be blank')
parser.add_argument(
    'game_name', help='This field cannot be blank')
parser.add_argument(
    'game_description', help='This field cannot be blank')
parser.add_argument(
    'game_image', help='This field cannot be blank')
parser.add_argument(
    'game_table', help='This field cannot be blank')


@jwt.token_in_blacklist_loader
def is_token_in_blacklist_loader(decrypted_token):
    return bool(Queries.select_token(decrypted_token['jti']))


class UserRegistration(Resource):

    def post(self):
        data = parser.parse_args()
        try:
            if Queries.select_user(username=data['username'], email=data['email']):
                return {'message': 'A user with the username {0} or email {1} already exists.'.format(data['username'], data['email'])}

            pasword_hash = pbkdf2_sha256.hash(data['password'])
            Queries.insert_user(
                data['username'], data['email'], pasword_hash)
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'User {0} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class UserLogin(Resource):

    def post(self):
        data = parser.parse_args()
        try:
            user = Queries.select_user(
                email=data['email'])
            if not user:
                return {'message': 'A user with the email {1} does not exist.'.format(data['email'])}

            if pbkdf2_sha256.verify(data['password'], user['password_hash']):
                access_token = create_access_token(identity=data['email'])
                refresh_token = create_refresh_token(identity=data['email'])
                return {
                    'message': 'Current user: {0} password: {1}'.format(user['email'], user['password_hash']),
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            else:
                return {'message': 'Login username/email and password pair are incorrect.'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class UserLogoutAccess(Resource):

    # @jwt_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            Queries.insert_token(token)
            return {'message': 'Access token is no longer valid.'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class UserLogoutRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            Queries.insert_token(token)
            return {'message': 'Refresh token is no longer valid.'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class Subscriptions(Resource):

    # @jwt_required
    def get(self):
        data = parser.parse_args()
        try:
            user_subscriptions = Queries.select_user_subscriptions(
                data['user_id'])
            return {
                'message': 'Successfully retrived user subscriptions!',
                'user_subscriptions': user_subscriptions
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            subscription_id = Queries.insert_subscription(
                data['user_id'], data['author_id'])
            return {
                'message': 'Successfully subscribed to this user!',
                'subscription_id': subscription_id
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            Queries.delete_subscription(data['subscription_id'])
            return {'message': 'Successfully unsubscribed from this user!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class Comment(Resource):

    def get(self):
        data = parser.parse_args()
        try:
            comments = Queries.select_comments(
                data['associated_id'])
            return {
                'message': 'Successfully retrived comments!',
                'comments': comments
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            comment_id, rating_id = Queries.insert_comment(
                data['associated_id'], data['user_id'], data['comment'], data['reply_id'])
            return {
                'message': 'Successfully inserted comment!',
                'comment_id': comment_id,
                'rating_id': rating_id
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500
    
    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_comment(data['comment_id'], data['comment'])
            return {'message': 'Successfully updated comment!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            Queries.delete_comment(data['comment_id'], data['rating_id'])
            return {'message': 'Successfully deleted comment!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class Rating(Resource):

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_rating(
                data['rating_id'], data['rate'], data['view'])
            return {'message': 'Successfully updated rating!'}
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500


class ForumPost(Resource):

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            post_id, rating_id = Queries.insert_forum_post(
                data['game_id'], data['user_id'], data['post_description'], data['post_text'])
            return {
                'message': 'Successfully inserted a new forum post!',
                'post_id': post_id,
                'rating_id': rating_id
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    def get(self):
        data = parser.parse_args()
        try:
            forum_post = Queries.select_forum_post(data['post_id'])
            return {
                'message': 'Successfully selected forum post!',
                'forum_post': forum_post
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_forum_post(
                data['post_id'], data['post_description'], data['post_text'])
            return {'message': 'Successfully updated forum post!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            Queries.delete_forum_post(data['post_id'], data['rating_id'])
            return {'message': 'Successfully deleted forum post!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class ForumPosts(Resource):

    def get(self):
        data = parser.parse_args()
        try:
            forum_posts = Queries.select_forum_posts(
                data['game_id'], data['hours'], data['order'], data['desending'])
            return {
                'message': 'Successfully selected forum posts!',
                'forum_posts': forum_posts
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class Build(Resource):

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            build_id, rating_id = Queries.insert_build(
                data['game_id'], data['build_description'], data['user_id'], data['build_markup'], data['image_url'])
            return {
                'message': 'Successfully inserted a new build!',
                'build_id': build_id,
                'rating_id': rating_id
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    def get(self):
        data = parser.parse_args()
        try:
            build = Queries.select_build(data['build_id'])
            return {
                'message': 'Successfully selected build!',
                'build': build
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_build(
                data['build_id'], data['build_description'], data['build_markup'], data['image_url'])
            return {'message': 'Successfully updated build!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            Queries.delete_build(data['build_id'], data['rating_id'])
            return {'message': 'Successfully deleted build!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class Builds(Resource):

    def get(self):
        data = parser.parse_args()
        try:
            builds = Queries.select_builds(
                data['game_id'], data['hours'], data['order'], data['desending'])
            return {
                'message': 'Successfully selected builds!',
                'builds': builds
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500


class Game(Resource):

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            game_id = Queries.insert_game(data['game_name'], data['game_description'], data['game_image'], data['game_table'])
            return {
                'message': 'Successfully inserted a new game!',
                'game_id': game_id
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    def get(self):
        try:
            games = Queries.select_games()
            return {
                'message': 'Successfully selected games!',
                'games': games
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_game(data['game_id'], data['game_name'], data['game_description'], data['game_image'], data['game_table'])
            return {'message': 'Successfully updated game!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            Queries.delete_game(data['game_id'])
            return {'message': 'Successfully deleted game!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class DS3Build(Resource):

    def get(self):
        data = parser.parse_args()
        try:
            build = DS3Queries.select_build(data['game_id'])
            return {
                'message': 'Successfully selected build!',
                'build': build
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            stat_allocation_id = DS3Queries.insert_build(
                data['build_id'], data['game_id'], data['stat_description'], data['item_description'],
                data['stats_dict'], data['item_list'], data['tag_list'])
            return {
                'message': 'Successfully inserted build!',
                'stat_allocation_id': stat_allocation_id
            }
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            DS3Queries.update_build(
                data['build_id'], data['stat_description'], data['item_description'])
            return {'message': 'Successfully updated build!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            DS3Queries.delete_build(data['game_id'])
            return {'message': 'Successfully deleted build!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class DS3BuildItem(Resource):

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            DS3Queries.insert_item_relationships(
                data['build_id'], data['item_list'])
            return {'message': 'Successfully inserted new build item!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            DS3Queries.delete_item_relationships(
                data['build_id'], data['item_list'])
            return {'message': 'Successfully deleted build item!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class DS3BuildTag(Resource):

    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            DS3Queries.insert_tag_relationships(
                data['build_id'], data['tag_list'])
            return {'message': 'Successfully inserted new build tag!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            DS3Queries.delete_tag_relationships(
                data['build_id'], data['tag_list'])
            return {'message': 'Successfully deleted build tag!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class DS3BuildStats(Resource):

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            DS3Queries.update_stat_allocation(
                data['stat_allocation_id'], data['stats_dict'])
            return {'message': 'Successfully updated build stats!'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500
