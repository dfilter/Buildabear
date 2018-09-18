from sqlalchemy import or_

from app.models import *
from app import db


class Queries:

    @staticmethod
    def insert_user(username, email, password_hash):
        new_user = User(username=username, email=email,
                        password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def select_user_credentials(username=None, email=None):
        user_credentials = User.query. \
            with_entities(User.username, User.email, User.password_hash). \
            filter(or_(User.username == username, User.email == email)).first()
        return UserSchema(many=False).dump(user_credentials).data

    @staticmethod
    def select_user(user_id=None, username=None, email=None):
        """ TODO: might need to remove password hash from the selected data """
        user = User.query. \
            filter(or_(User.user_id == user_id, User.username ==
                       username, User.email == email)).first()
        return UserSchema(many=False).dump(user).data

    @staticmethod
    def insert_subscription(user_id, author_id):
        new_subscription = UserSubscriptions(
            user_id=user_id, author_id=author_id)
        db.session.add(new_subscription)
        db.session.commit()

    @staticmethod
    def select_user_subscriptions(user_id):
        subscriptions = UserSubscriptions.query. \
            join(User, User.user_id == UserSubscriptions.author_id).\
            with_entities(
                User.user_id,
                User.username,
                User.date_joined,
                User.subscriber_count,
                User.user_level). \
            order_by(User.username).all()
        return UserSchema(many=True).dump(subscriptions).data

    @staticmethod
    def insert_comment(associated_id, user_id, comment, reply_id=None):
        new_rating = Rating(associated_id=associated_id)
        db.session.add(new_rating)
        db.session.commit()
        new_comment = Comment(
            associated_id=associated_id,
            user_id=user_id,
            reply_id=reply_id,
            comment=comment,
            rating_id=new_rating.rating_id)
        db.session.add(new_comment)
        db.session.commit()

    @staticmethod
    def select_comments(associated_id):
        comments = Comment.query. \
            join(Rating, Comment.rating_id == Rating.rating_id). \
            join(User, Comment.user_id == User.user_id). \
            add_columns(
                Comment.comment_id,
                Comment.date_posted,
                Comment.comment,
                Comment.associated_id,
                Comment.rating_id,
                Comment.user_id,
                Comment.reply_id,
                User.username,
                Rating.likes,
                Rating.dislikes). \
            filter(Comment.associated_id == associated_id). \
            order_by(Comment.date_posted).all()
        return CommentsSchema(many=True).dump(comments).data

    @staticmethod
    def update_rating(rating_id, like=None, dislike=None, view=None):
        rating = Rating.query.filter(Rating.rating_id == rating_id).first()
        if like:
            rating.likes += like
        if dislike:
            rating.dislikes += dislike
        if view:
            rating.views += view
        db.session.commit()


if __name__ == '__main__':
    print Queries.insert_subscription(1, 1)
