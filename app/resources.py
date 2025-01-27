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

# below are all the arguments that the json parser will look for the in 
# body of any http request made, or any parameters in the url.
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
parser.add_argument(
    'down_vote', help='This field cannot be blank')
parser.add_argument(
    'up_vote', help='This field cannot be blank')
parser.add_argument(
    'user_description', help='This field cannot be blank')
parser.add_argument(
    'user_level', help='This field cannot be blank')

# This method decripts the token and returns True if is successful and False if it is not
@jwt.token_in_blacklist_loader
def is_token_in_blacklist_loader(decrypted_token):
    return bool(Queries.select_token(decrypted_token['jti']))


class UserRegistration(Resource):
    """
    Passed the Resource class imported from the flask_restul package
    This class handels post requests made regarding registration.
    It will return a message and the user object including the access
    and refresh tokens. Passwords are not stored as plain test they are hashed
    using SHA256 hashing algorythm
    """

    def post(self):
        data = parser.parse_args()
        try:
            if Queries.select_user(username=data['username'], email=data['email']):
                return {'message': 'A user with the username {0} or email {1} already exists.'.format(data['username'], data['email'])}

            pasword_hash = pbkdf2_sha256.hash(data['password'])
            Queries.insert_user(
                data['username'], data['email'], pasword_hash)
            user = Queries.select_user(
                email=data['email'])
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            user['access_token'] = access_token
            user['refresh_token'] = refresh_token
            return {
                'message': 'User {0} was created'.format(data['username']),
                'user': user
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500


class UserLogin(Resource):
    """
    Handels post requests made regarding user login, retrives all the 
    relevent data related to that user.
    """

    def post(self):
        data = parser.parse_args()
        try:
            user = Queries.select_user(
                email=data['email'])
            if not user:
                return {'message': 'A user with the email {0} does not exist.'.format(data['email'])}, 200

            if pbkdf2_sha256.verify(data['password'], user['password_hash']):
                access_token = create_access_token(identity=data['email'])
                refresh_token = create_refresh_token(identity=data['email'])
                subscriptions = Queries.select_subscription_list(user['user_id'])
                user['access_token'] = access_token
                user['refresh_token'] = refresh_token
                user['subscriptions'] = subscriptions
                return {
                    'message': 'Current user: {0} password: {1}'.format(user['email'], user['password_hash']),
                    'user': user
                }, 200
            else:
                return {'message': 'Login username/email and password pair are incorrect.'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class CheckUser(Resource):
    """
    This class handels the first step of user password recovery, and checks to see that the
    username and email passed is correct.
    """

    def post(self):
        data = parser.parse_args()
        try:
            user = Queries.select_user(
                email=data['email'], username=data['username'])
            if user:
                return {
                    'message': 'Please enter your new password to complete the password reset process.',
                    'continue': True
                }
            else:
                return {
                    'message': 'Could not find the provided credentials please try again',
                    'continue': False
                }
        
        except Exception as e:
            print e
            return {
                'message': 'Something went wrong!',
                'continue': False
            }, 500


class ResetPassword(Resource):
    """
    This class handels the second portion of password recovery,
    it simply hashes the new password and inserts it into the users table.
    Returns appropriate messages if anything goes wrong.
    """

    def post(self):
        data = parser.parse_args()
        try:
            pasword_hash = pbkdf2_sha256.hash(data['password'])
            Queries.update_user(username=data['username'], password_hash=pasword_hash)
            return {
                'message': 'Your password has successfully been reset. Please proceed to login.',
                'continue': True
            }      
        
        except Exception as e:
            if e:
                print e
                return {
                    'message': 'Something went wrong!',
                    'continue': False
                }, 500
            else:
                return {
                    'message': 'Could not update password.',
                    'continue': False
                }
            


class UserLogoutAccess(Resource):
    """
    This class handles logout and invalidates a users access token.
    """

    # @jwt_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            Queries.insert_token(token)
            return {'message': 'Access token is no longer valid.'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class UserLogoutRefresh(Resource):
    """
    This class handles invalidating a users refresh token when logging out.
    """

    @jwt_refresh_token_required
    def post(self):
        token = get_raw_jwt()['jti']
        try:
            Queries.insert_token(token)
            return {'message': 'Refresh token is no longer valid.'}
        except Exception as e:
            return {'message': 'Something went wrong!'}, 500


class TokenRefresh(Resource):
    """
    This class provides the user with a new access token
    """

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class User(Resource):
    """
    This class simply retrives a users information given their user_id
    """

    # @jwt_required
    def get(self):
        data = parser.parse_args()
        try:
            user = Queries.select_user(data['user_id'])
            return {
                'message': 'Successfully retrived user info!',
                'user': user
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500


class Profile(Resource):
    """
    This class handles profile CRUD requests.
    The get method will return all the data accociated with a user's profile.
    The put method will update a user's information such as email, username, user description or level.
    The delete method will delete the user who's id is passed.
    """

    # @jwt_required
    def get(self):
        data = parser.parse_args()
        try:
            user_profile = Queries.select_user(data['user_id'], data['username'], data['email'])
            user_posts = Queries.select_user_posts(data['user_id'])
            user_builds = Queries.select_user_builds(data['user_id'])
            user_subscriptions = Queries.select_user_subscriptions(data['user_id'])
            user_profile['forum_posts'] = user_posts
            user_profile['user_builds'] = user_builds
            user_profile['user_subscriptions'] = user_subscriptions
            return {
                'message': 'Successfully retrived user info!',
                'user_profile': user_profile
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_user(user_id=data['user_id'], username=data['username'], email=data['email'], user_level=data['user_level'], user_description=data['user_description'])
            return {
                'message': 'Successfully updated user!',
                'success': True
            }
        except Exception as e:
            print e
            return {
                'message': 'Something went wrong!',
                'success': False
            }, 500

    # @jwt_required
    def delete(self):
        data = parser.parse_args()
        try:
            Queries.delete_user(data['user_id'])
            return {
                'message': 'Successfully deleted user!',
                'success': True
            }
        except Exception as e:
            print e
            return {
                'message': 'Something went wrong!',
                'success': False
            }, 500


class Profiles(Resource):
    """
    Not used
    """

    # @jwt_required
    def get(self):
        data = parser.parse_args()
        try:
            user_profiles = Queries.select_users(data['username'], data['email'])
            return {
                'message': 'Successfully retrived user info!',
                'user_profiles': user_profiles
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500


class Subscriptions(Resource):
    """
    This class handles the CRUD requests for all types of subscription
    The get method will get all the subscriptions associated with a user_id.
    The post method will create a new subscription to another user.
    The delete methof will delete a subscrption to another user.
    """

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
    """
    This class handels all the CRUD requests regarding comments.
    The get method will select all the comments accociated with a build or forum post.
    The post method will create a new comment and return it
    The put method will update a comment text.
    The delete method will simply delete the comment and the associated rating records.
    """

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
                data['associated_id'], data['user_id'], data['comment'])  # add back , data['reply_id'] if you end up adding replies
            comment = Queries.select_comment(comment_id)
            return {
                'message': 'Successfully inserted comment!',
                'comment': comment
            }
        except Exception as e:
            print e
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
    """
    This class simply updates ratings for builds, forum posts and comments on a put request.
    """

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_rating(
                data['rating_id'], data['down_vote'], data['up_vote'], data['view'])
            return {'message': 'Successfully updated rating!'}
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500


class ForumPost(Resource):
    """
    This class handles the CRUD for forum posts.
    The post method will create a new forum post.
    The get method will get a specific forum post using post_id.
    The put method will update a specidied forum post.
    The delete mthod will delete a specidied forum post.
    """

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
            post_comments = Queries.select_comments(data['post_id'])
            forum_post['comments'] = post_comments
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
    """
    This Class will retrive all the forum posts for a spcified game, time range
    and will order the results based on parameters passed from the frontend request.
    """

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
    """
    This class handles the CRUD for buids.
    The post method will create a new build.
    The get method will get a specific build using build_id.
    The put method will update a specidied build, given the build_id and what to update.
    The delete mthod will delete a specidied build, given the build_id.
    """

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
            build_comments = Queries.select_comments(data['build_id'])
            build['comments'] = build_comments
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
    """
    This Class will retrive all the builds for a spcified game, time range
    and will order the results based on parameters passed from the frontend request.
    """

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
    """
    This class handles the CRUD for games.
    The post method will create a new game.
    The get method will get a specific game using game_id.
    The put method will update a specidied game, given the game_id and what to update.
    The delete mthod will delete a specidied game, given the game_id.
    """
    
    # @jwt_required
    def post(self):
        data = parser.parse_args()
        try:
            game_id = Queries.insert_game(
                data['game_name'], data['game_description'], data['game_image'], data['game_table'])
            return {
                'message': 'Successfully inserted a new game!',
                'game_id': game_id
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    def get(self):
        data = parser.parse_args()
        try:
            game = Queries.select_game(data['game_id'])
            return {
                'message': 'Successfully selected games!',
                'game': game
            }
        except Exception as e:
            print e
            return {'message': 'Something went wrong!'}, 500

    # @jwt_required
    def put(self):
        data = parser.parse_args()
        try:
            Queries.update_game(data['game_id'], data['game_name'],
                                data['game_description'], data['game_image'], data['game_table'])
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


class Games(Resource):
    """
    This Class simmply returns all games on a get request.
    """

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

""" 
None of the following classes are requested from the fronted as I ran out of time and was unable to impliment them.
"""

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
