from sqlalchemy import or_, Table
from datetime import datetime, timedelta

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
    def update_user(user_id, username, email, user_level):
        user_edit = User.query.filter(User.user_id == user_id).first()
        user_edit.username = username
        user_edit.email = email
        user_edit.user_level = user_level
        db.session.commit()

    @staticmethod
    def delete_user(user_id):
        User.query.filter(User.user_id == user_id).delete()
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
        add_subscriber = User.query. \
            filter(User.user_id == author_id).first()
        add_subscriber.subscriber_count += 1
        db.session.add(new_subscription)
        db.session.commit()

    @staticmethod
    def delete_subscription(subscription_id):
        UserSubscriptions.query.filter(
            UserSubscriptions.subscription_id == subscription_id).delete()
        db.session.commit()

    @staticmethod
    def select_user_subscriptions(user_id):
        subscriptions = UserSubscriptions.query. \
            join(User, User.user_id == UserSubscriptions.author_id).\
            with_entities(
                UserSubscriptions.subscription_id,
                User.user_id,
                User.username,
                User.date_joined,
                User.subscriber_count,
                User.user_level). \
            order_by(User.username). \
            filter(UserSubscriptions.user_id == user_id).all()
        return UserSubscriptionsSchema(many=True).dump(subscriptions).data

    @staticmethod
    def insert_comment(associated_id, user_id, comment, reply_id=None):
        """ TODO: switch to using triggers to insert rating? """
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
    def update_comment(comment_id, comment):
        comment_edit = Comment.query.filter(
            Comment.comment_id == comment_id).first()
        comment_edit.comment = comment
        comment_edit.date_posted = datetime.utcnow()
        db.session.commit()

    @staticmethod
    def delete_comment(comment_id, rating_id):
        """ TODO: switch to using triggers to delete rating? """
        Comment.query.filter(Comment.comment_id == comment_id).delete()
        Rating.query.filter(Rating.rating_id == rating_id).delete()
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
                Rating.rating). \
            filter(Comment.associated_id == associated_id). \
            order_by(Comment.date_posted).all()
        return CommentsSchema(many=True).dump(comments).data

    @staticmethod
    def update_rating(rating_id, rate=None, view=None):
        rating = Rating.query.filter(Rating.rating_id == rating_id).first()
        if rate:
            rating.rating += rate
        if view:
            rating.views += view
        db.session.commit()

    @staticmethod
    def insert_forum_post(game_id, user_id, post_description, post_text):
        """ TODO: switch to using triggers to insert rating? """
        new_rating = Rating()
        db.session.add(new_rating)
        db.session.commit()
        new_forum_post = ForumPost(
            game_id=game_id,
            rating_id=new_rating.rating_id,
            post_description=post_description,
            post_text=post_text,
            author_id=user_id)
        db.session.add(new_forum_post)
        db.session.commit()
        add_associate_id = Rating.query.filter(
            Rating.rating_id == new_rating.rating_id).first()
        add_associate_id.associated_id = new_forum_post.post_id
        db.session.commit()

    @staticmethod
    def select_forum_posts(game_id, hours=8766, order=None, desending=True):
        """ Dynamically selecting forum posts based on passed parameters """
        today_datetime = datetime.utcnow()
        delta_time = today_datetime - timedelta(hours=hours)
        forum_posts = ForumPost.query. \
            join(Rating, ForumPost.rating_id == Rating.rating_id). \
            join(User, ForumPost.author_id == User.user_id). \
            add_columns(
                ForumPost.post_id,
                ForumPost.rating_id,
                ForumPost.game_id,
                ForumPost.post_description,
                ForumPost.date_posted,
                Rating.rating,
                Rating.views,
                User.username). \
            filter(ForumPost.game_id == game_id). \
            filter(ForumPost.date_posted > delta_time)
        if order in ['rating', 'views']:
            if desending:
                forum_posts = forum_posts.order_by(
                    getattr(Rating, order).desc())
            else:
                forum_posts = forum_posts.order_by(getattr(Rating, order))
        elif order:
            if desending:
                forum_posts = forum_posts.order_by(
                    getattr(ForumPost, order).desc())
            else:
                forum_posts = forum_posts.order_by(getattr(ForumPost, order))
        forum_posts = forum_posts.all()
        return ForumPostRatingSchema(many=True).dump(forum_posts).data

    @staticmethod
    def select_forum_post(post_id):
        forum_post = ForumPost.query. \
            join(Rating, ForumPost.rating_id == Rating.rating_id). \
            join(User, ForumPost.author_id == User.user_id). \
            add_columns(
                ForumPost.post_id,
                ForumPost.rating_id,
                ForumPost.game_id,
                ForumPost.post_description,
                ForumPost.date_posted,
                Rating.rating,
                Rating.views,
                User.username). \
            filter(ForumPost.post_id == post_id).first()
        return ForumPostRatingSchema(many=False).dump(forum_post).data

    @staticmethod
    def update_forum_post(post_id, post_description=None, post_text=None):
        forum_post = ForumPost.query.filter(
            ForumPost.post_id == post_id).first()
        if post_description:
            forum_post.post_description = post_description
        if post_text:
            forum_post.post_text = post_text
        db.session.commit()

    @staticmethod
    def delete_forum_post(post_id, rating_id):
        ForumPost.query.filter(ForumPost.post_id == post_id).delete()
        Rating.query.filter(Rating.rating_id == rating_id).delete()
        db.session.commit()

    @staticmethod
    def insert_build(game_id, build_description, user_id, build_markup, image_url):
        new_rating = Rating()
        db.session.add(new_rating)
        db.session.commit()
        new_build = Build(
            build_description=build_description,
            build_markup=build_markup,
            rating_id=new_rating.rating_id,
            game_id=game_id,
            author_id=user_id,
            image_url=image_url)
        db.session.add(new_build)
        db.session.commit()
        add_associate_id = Rating.query.filter(
            Rating.rating_id == new_rating.rating_id).first()
        add_associate_id.associated_id = new_build.post_id
        db.session.commit()

    @staticmethod
    def select_builds(game_id, hours=8766, order=None, desending=True):
        today_datetime = datetime.utcnow()
        delta_time = today_datetime - timedelta(hours=hours)
        game_builds = Build.query. \
            join(Rating, ForumPost.rating_id == Rating.rating_id). \
            join(User, ForumPost.author_id == User.user_id). \
            add_columns(
                Build.build_id,
                Build.rating_id,
                Build.author_id,
                Build.game_id,
                Build.build_description,
                Build.build_markup,
                Build.image_url,
                Build.date_posted,
                Rating.rating,
                Rating.views,
                User.username). \
            filter(Build.game_id == game_id). \
            filter(Build.date_posted > delta_time)
        if order in ['rating', 'views']:
            if desending:
                game_builds = game_builds.order_by(
                    getattr(Rating, order).desc())
            else:
                game_builds = game_builds.order_by(getattr(Rating, order))
        elif order:
            if desending:
                game_builds = game_builds.order_by(
                    getattr(Build, order).desc())
            else:
                game_builds = game_builds.order_by(getattr(Build, order))
        game_builds = game_builds.all()
        return BuildRatingSchema(many=True).dump(game_builds).data

    @staticmethod
    def update_build(build_id, build_description=None, build_markup=None, image_url=None):
        build = Build.query.filter(Build.build_id == build_id).first()
        if build_description:
            build.build_description = build_description
        if build_markup:
            build.build_markup = build_markup
        if image_url:
            build.image_url = image_url
        db.session.commit()

    @staticmethod
    def delete_build(build_id, rating_id):
        Build.query.filter(Build.build_id == build_id).delete()
        Rating.query.filter(Rating.rating_id == rating_id).delete()
        db.session.commit()

    @staticmethod
    def insert_game(game_name, game_description, game_image, game_table):
        new_game = Game(
            game_name=game_name,
            game_description=game_description,
            game_image=game_image,
            game_table=game_table)
        db.session.add(new_game)
        db.session.commit()

    @staticmethod
    def select_games():
        games = Game.query.all()
        return GameSchema(many=True).dump(games).data

    @staticmethod
    def update_game(game_id, game_name=None, game_description=None, game_image=None, game_table=None):
        game = Game.query.filter(Game.game_id == game_id).first()
        if game_name:
            game.game_name = game_name
        if game_description:
            game.game_description = game_description
        if game_image:
            game.game_image = game_image
        if game_table:
            game.game_table = game_table
        db.session.commit()

    @staticmethod
    def delete_game(game_id):
        Game.query.filter(Game.game_id == game_id).delete()
        db.session.commit()


if __name__ == '__main__':
    pass
    # Queries.insert_user('jdoe', 'john.doe@something.com', 'Password#')
    # Queries.insert_forum_post(2, 'Description for game 2.')
    # print Queries.select_forum_posts(
    #     1, hours=8766, order="date_posted", desending=True)
    # Queries.update_rating(2, rate=1, view=2)
    # Queries.delete_forum_post(4, 4)
    # print Queries.select_forum_post(1)
    # Queries.insert_build(1, 1, "Build Description", "")
    # print = Queries.select_user(username="test")
