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
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(16), unique=True)
    date_joined = db.Column(db.DateTime,
                            default=datetime.utcnow)
    subscriber_count = db.Column('subscriber_count', db.Integer, default=0)
    email = db.Column(db.String(16), unique=True)
    user_level = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128), nullable=False)


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
    rating = fields.Integer()


class ForumPost(db.Model):
    __tablename__ = 'forum_post'
    post_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    rating_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_description = db.Column(db.Text)
    post_text = db.Column(db.Text)


class ForumPostRatingSchema(ma.Schema):
    post_id = fields.Integer()
    game_id = fields.Integer()
    rating_id = fields.Integer()
    date_posted = fields.DateTime()
    post_description = fields.String()
    rating_id = fields.Integer()
    author_id = fields.Integer()
    rating = fields.Integer()
    views = fields.Integer()
    username = fields.String()


class ForumPostSchema(ma.ModelSchema):
    class Meta:
        model = ForumPost


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    associated_id = db.Column(db.Integer)
    rating = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)


class Build(db.Model):
    __tablename__ = 'build'
    build_id = db.Column(db.Integer, primary_key=True)
    build_description = db.Column(db.Text)
    build_markup = db.Column(db.Text)
    rating_id = db.Column(db.Integer)
    game_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)


class BuildRatingSchema(ma.Schema):
    build_id = fields.Integer()
    game_id = fields.Integer()
    rating_id = fields.Integer()
    date_posted = fields.DateTime()
    image_url = fields.String()
    build_description = fields.String()
    build_markup = fields.String()
    rating_id = fields.Integer()
    author_id = fields.Integer()
    rating = fields.Integer()
    views = fields.Integer()
    username = fields.String()


class Game(db.Model):
    __tablename__ = 'game'
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(128))
    game_description = db.Column(db.Text)
    game_image = db.Column(db.Text)
    game_table = db.Column(db.String(255))


class GameSchema(ma.ModelSchema):
    class Meta:
        model = Game


class DS3Build(db.Model):
    __tablename__ = 'DS3_build'
    build_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    stat_allocation_id = db.Column(db.Integer)
    stat_description = db.Column(db.Text)
    item_csv = db.Column(db.Text)
    tag_csv = db.Column(db.Text)
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
