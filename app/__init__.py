from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_restful import Api
from flask_restful.utils import cors
from flask_jwt_extended import JWTManager
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
api = Api(app)
api.decorators=[cors.crossdomain(origin='*')]
jwt = JWTManager(app)

from app import routes, models, resources

api.add_resource(resources.UserRegistration, '/registration')
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
api.add_resource(resources.DS3Build, '/ds3build')
api.add_resource(resources.DS3BuildItem, '/ds3buildItem')
api.add_resource(resources.DS3BuildTag, '/ds3buildTag')
api.add_resource(resources.DS3BuildStats, '/ds3buildStats')
