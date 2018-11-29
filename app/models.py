from datetime import datetime
from marshmallow import fields

from app import db, ma

"""
TODO: 
1. Add relationships
2. Make sure data types are correct
3. Additional requirements
"""


class RevokedToken(db.Model):
    __tablename__ = 'revoked_token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)
    subscriber_count = db.Column(db.Integer, default=0)
    user_description = db.Column(db.Text)
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
    down_vote = fields.Integer()
    up_vote = fields.Integer()


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
    post_text= fields.String()
    author_id = fields.Integer()
    down_vote = fields.Integer()
    up_vote = fields.Integer()
    views = fields.Integer()
    username = fields.String()


class ForumPostSchema(ma.ModelSchema):
    class Meta:
        model = ForumPost


class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    associated_id = db.Column(db.Integer)
    down_vote = db.Column(db.Integer, default=0)
    up_vote = db.Column(db.Integer, default=0)
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
    author_id = fields.Integer()
    down_vote = fields.Integer()
    up_vote = fields.Integer()
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


class DS3StatAllocation(db.Model):
    __tablename__ = 'DS3_stat_allocation'
    stat_allocation_id = db.Column(db.Integer, primary_key=True)
    build_id = db.Column(db.Integer, db.ForeignKey(
        'DS3_build.build_id'), unique=True)
    luck = db.Column(db.Integer)
    faith = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    vitality = db.Column(db.Integer)
    endurance = db.Column(db.Integer)
    attunement = db.Column(db.Integer)
    vigor = db.Column(db.Integer)


class DS3StatAllocationSchema(ma.ModelSchema):
    class Meta:
        model = DS3StatAllocation


class DS3Tag(db.Model):
    __tablename__ = 'DS3_tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text)


class DS3TagSchema(ma.ModelSchema):
    class Meta:
        model = DS3Tag


class DS3Item(db.Model):
    __tablename__ = 'DS3_item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)


class DS3ItemSchema(ma.ModelSchema):
    class Meta:
        model = DS3Item


DS3_item_relationships = db.Table(
    'DS3_item_relationships',
    db.Column('build_id', db.Integer, db.ForeignKey('DS3_build.build_id')),
    db.Column('item_id', db.Integer, db.ForeignKey('DS3_item.item_id'))
)


DS3_tag_relationships = db.Table(
    'DS3_tag_relationships',
    db.Column('build_id', db.Integer, db.ForeignKey('DS3_build.build_id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('DS3_tag.tag_id'))
)


class DS3Build(db.Model):
    __tablename__ = 'DS3_build'
    build_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    stat_description = db.Column(db.Text)
    item_description = db.Column(db.Text)
    stats = db.relationship('DS3StatAllocation',
                            backref='build', lazy=True)
    items = db.relationship('DS3Item', secondary=DS3_item_relationships,
                            backref=db.backref('build_items', lazy='dynamic'))
    tags = db.relationship('DS3Tag', secondary=DS3_tag_relationships,
                           backref=db.backref('build_tags', lazy='dynamic'))


class DS3BuildSchema(ma.ModelSchema):
    tags = ma.Nested(DS3TagSchema, many=True)
    items = ma.Nested(DS3ItemSchema, many=True)
    stats = ma.Nested(DS3StatAllocationSchema, many=True)

    class Meta:
        model = DS3Build
