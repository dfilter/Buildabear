from datetime import datetime
from marshmallow import fields

from app import db, ma

"""
TODO: 
1. Add relationships
2. Make sure data types are correct
3. Additional requirements
"""


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(16), unique=True)
    date_joined = db.Column('date_joined', db.DateTime,
                            default=datetime.utcnow)
    subscriber_count = db.Column('subscriber_count', db.Integer, default=0)
    email = db.Column('email', db.String(16), unique=True)
    user_level = db.Column('user_level', db.Integer, default=0)
    password_hash = db.Column('password_hash', db.String(128))


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class UserSubscriptions(db.Model):
    __tablename__ = 'user_subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)


class UserSubscriptionsSchema(ma.Schema):
    subscription_id = fields.Integer()
    user_id = fields.Integer()
    subscriber_count = fields.Integer()
    username = fields.String()
    date_joined = fields.DateTime()
    user_level = fields.Integer()


class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer, default=0)
    associated_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    reply_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text)


class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment


class CommentsSchema(ma.Schema):
    comment_id = fields.Integer()
    rating_id = fields.String()
    associated_id = fields.Integer()
    user_id = fields.Integer()
    username = fields.String()
    reply_id = fields.Integer()
    date_posted = fields.DateTime()
    comment = fields.String()
    likes = fields.Integer()
    dislikes = fields.Integer()


class ForumPost(db.Model):
    __tablename__ = 'forum_post'
    post_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    rating_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime)
    post_description = db.Column(db.Text)


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    associated_id = db.Column(db.Integer)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)


class Build(db.Model):
    __tablename__ = 'build'
    build_id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    build_description = db.Column(db.Text)
    build_walkthrough = db.Column(db.Text)
    date = db.Column(db.DateTime)


class Game(db.Model):
    __tablename__ = 'game'
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(128))
    game_description = db.Column(db.Text)
    game_image = db.Column(db.Text)


class DS3Build(db.Model):
    __tablename__ = 'DS3_build'
    build_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    stat_allocation_id = db.Column(db.Integer)
    item_csv = db.Column(db.Text)
    tag_csv = db.Column(db.Text)
    build_description = db.Column(db.Text)
    item_description = db.Column(db.Text)


class DS3StatAllocation(db.Model):
    __tablename__ = 'DS3_stat_allocation'
    stat_allocation_id = db.Column(db.Integer, primary_key=True)
    luck = db.Column(db.Integer)
    faith = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    vitality = db.Column(db.Integer)
    endurance = db.Column(db.Integer)
    attunement = db.Column(db.Integer)
    vigor = db.Column(db.Integer)


class DS3Tags(db.Model):
    __tablename__ = 'DS3_tags'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text)


class DS3Item(db.Model):
    __tablename__ = 'DS3_items'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)
