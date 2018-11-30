from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)


from app import routes, models, resources


api.add_resource(resources.UserRegistration, '/register')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.Subscriptions, '/subscription')
api.add_resource(resources.Comment, '/comment')
api.add_resource(resources.Rating, '/rating')
api.add_resource(resources.ForumPost, '/forumPost')
api.add_resource(resources.ForumPosts, '/forumPosts')
api.add_resource(resources.Build, '/build')
api.add_resource(resources.Builds, '/builds')
api.add_resource(resources.Game, '/game')
api.add_resource(resources.Games, '/games')
api.add_resource(resources.DS3Build, '/ds3build')
api.add_resource(resources.DS3BuildItem, '/ds3buildItem')
api.add_resource(resources.DS3BuildTag, '/ds3buildTag')
api.add_resource(resources.DS3BuildStats, '/ds3buildStats')
api.add_resource(resources.Profile, '/profile')
api.add_resource(resources.Profiles, '/profiles')
api.add_resource(resources.CheckUser, '/checkuser')
api.add_resource(resources.ResetPassword, '/resetpassword')
api.add_resource(resources.User, '/user')
