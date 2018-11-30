from datetime import datetime
from marshmallow import fields

from app import db, ma


"""
In essense the following models are much like the classes used in 
Entity Framework, they reflect the tables they are associated with.
"""

""" Model for the revoked_token table. Class reflects 
the table and is used by Flask-SQLAlchemy to make queries """
class RevokedToken(db.Model):
    __tablename__ = 'revoked_token'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)


""" Model for the user table. Class reflects the table. """
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


""" This Schema class is used to serialize (give properties) to the 
values of the associated Class tabel in this case the User class 
wich reflects the user table. """
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


""" Model for the user_subscriptions table. Class reflects the table. """
class UserSubscriptions(db.Model):
    __tablename__ = 'user_subscriptions'
    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)


""" Schema used to serialze joins between mutiple classes. """
class UserSubscriptionsSchema(ma.Schema):
    subscription_id = fields.Integer()
    user_id = fields.Integer()
    subscriber_count = fields.Integer()
    username = fields.String()
    date_joined = fields.DateTime()
    user_level = fields.Integer()


""" Model for the comment table. Class reflects the table. """
class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, primary_key=True)
    rating_id = db.Column(db.Integer, default=0)
    associated_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    reply_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    comment = db.Column(db.Text)


""" Schema used to serialze the Comment class. """
class CommentSchema(ma.ModelSchema):
    class Meta:
        model = Comment


""" Schema used to serialze joins between mutiple classes. """
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


""" Model for the forum_post table. Class reflects the table. """
class ForumPost(db.Model):
    __tablename__ = 'forum_post'
    post_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer)
    rating_id = db.Column(db.Integer)
    author_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    post_description = db.Column(db.Text)
    post_text = db.Column(db.Text)


""" Schema used to serialze joins between mutiple classes. """
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


""" Schema used to serialize the data of the ForumPost class after a qeuery is made. """
class ForumPostSchema(ma.ModelSchema):
    class Meta:
        model = ForumPost


""" Model for the rating table. Class reflects the table. """
class Rating(db.Model):
    __tablename__ = 'rating'
    rating_id = db.Column(db.Integer, primary_key=True)
    associated_id = db.Column(db.Integer)
    down_vote = db.Column(db.Integer, default=0)
    up_vote = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)


""" Model for the build table. Class reflects the table. """
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


""" Schema used to serialze joins between mutiple classes. """
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


""" Model for the game table. Class reflects the table. """
class Game(db.Model):
    __tablename__ = 'game'
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(128))
    game_description = db.Column(db.Text)
    game_image = db.Column(db.Text)
    game_table = db.Column(db.String(255))


""" Schema used to serialize the data of the Game class after a qeuery is made. """
class GameSchema(ma.ModelSchema):
    class Meta:
        model = Game


""" Model for the DS3_stat_allocation table. Class reflects the table. """
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


""" Schema used to serialize the data of the DS3StatAllocation class after a qeuery is made. """
class DS3StatAllocationSchema(ma.ModelSchema):
    class Meta:
        model = DS3StatAllocation


""" Model for the DS3_tag table. Class reflects the table. """
class DS3Tag(db.Model):
    __tablename__ = 'DS3_tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.Text)


""" Schema used to serialize the data of the DS3Tag class after a qeuery is made. """
class DS3TagSchema(ma.ModelSchema):
    class Meta:
        model = DS3Tag


""" Model for the DS3_item table. Class reflects the table. """
class DS3Item(db.Model):
    __tablename__ = 'DS3_item'
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.Text)


""" Schema used to serialize the data of the DS3Item class after a qeuery is made. """
class DS3ItemSchema(ma.ModelSchema):
    class Meta:
        model = DS3Item

""" Here the table is created as a variable which is used in a many to many
relactionship with the DS3Build class. """
DS3_item_relationships = db.Table(
    'DS3_item_relationships',
    db.Column('build_id', db.Integer, db.ForeignKey('DS3_build.build_id')),
    db.Column('item_id', db.Integer, db.ForeignKey('DS3_item.item_id'))
)

""" Table created as a variable. """
DS3_tag_relationships = db.Table(
    'DS3_tag_relationships',
    db.Column('build_id', db.Integer, db.ForeignKey('DS3_build.build_id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('DS3_tag.tag_id'))
)


""" Model for the DS3_build table. Class reflects the table. Here we have a one
to many relationship with the DS3StatAllocation class, and a many to many relationship
with the DS3_item_relationships and DS3_tag_relationships tabels initialized as veriables. """
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

""" Schema used to serialize the data of the DS3Build class after a qeuery is made. """
class DS3BuildSchema(ma.ModelSchema):
    tags = ma.Nested(DS3TagSchema, many=True)
    items = ma.Nested(DS3ItemSchema, many=True)
    stats = ma.Nested(DS3StatAllocationSchema, many=True)

    class Meta:
        model = DS3Build
