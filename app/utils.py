from sqlalchemy import or_, Table
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta

from app.models import *
from app import db


class Queries:

    @staticmethod
    def insert_token(token):
        new_token = RevokedToken(token=token)
        db.session.add(new_token)
        db.session.commit()

    @staticmethod
    def select_token(token):
        return RevokedToken.query.filter(RevokedToken.token == token).first()

    @staticmethod
    def insert_user(username, email, password_hash):
        new_user = User(username=username, email=email,
                        password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def update_user(user_id=None, username=None, email=None, user_level=None, password_hash=None):
        user_edit = User.query.filter(or_(User.user_id == user_id, User.username == username)).first()
        if username:
            user_edit.username = username
        if email:
            user_edit.email = email
        if user_level:
            user_edit.user_level = user_level
        if password_hash:
            user_edit.password_hash = password_hash
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
    def select_users(username=None, email=None):
        user = User.query. \
            filter(or_(User.username.like('%' + str(username) + '%'), User.email.like('%' + str(email) + '%'))).first()
        return UserSchema(many=False).dump(user).data

    @staticmethod
    def select_user_builds(user_id):
        user_builds = Build.query. \
            join(Rating, Build.rating_id == Rating.rating_id). \
            join(User, Build.author_id == User.user_id). \
            add_columns(
                Build.build_id,
                Build.rating_id,
                Build.author_id,
                Build.game_id,
                Build.build_description,
                Build.build_markup,
                Build.image_url,
                Build.date_posted,
                Rating.down_vote,
                Rating.up_vote,
                Rating.views,
                User.username). \
            filter(Build.author_id == user_id).all()
        return BuildRatingSchema(many=True).dump(user_builds).data

    @staticmethod
    def select_user_posts(user_id):
        user_posts = ForumPost.query. \
            join(Rating, ForumPost.rating_id == Rating.rating_id). \
            join(User, ForumPost.author_id == User.user_id). \
            add_columns(
                ForumPost.post_id,
                ForumPost.rating_id,
                ForumPost.game_id,
                ForumPost.author_id,
                ForumPost.post_description,
                ForumPost.date_posted,
                Rating.down_vote,
                Rating.up_vote,
                Rating.views,
                User.username). \
            filter(ForumPost.author_id == user_id).all()
        return ForumPostRatingSchema(many=True).dump(user_posts).data

    @staticmethod
    def insert_subscription(user_id, author_id):
        new_subscription = UserSubscriptions(
            user_id=user_id, author_id=author_id)
        add_subscriber = User.query. \
            filter(User.user_id == author_id).first()
        add_subscriber.subscriber_count += 1
        db.session.add(new_subscription)
        db.session.commit()
        return new_subscription.subscription_id

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
    def select_subscription_list(user_id):
        subscriptions = db.session.query(UserSubscriptions.author_id). \
            filter(UserSubscriptions.user_id == user_id).all()
        temp_list = []
        for item in subscriptions:
            temp_list.append(item[0])
        return temp_list

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
        return new_comment.comment_id, new_rating.rating_id

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
                Rating.down_vote,
                Rating.up_vote). \
            filter(Comment.associated_id == associated_id). \
            order_by(Comment.date_posted).all()
        return CommentsSchema(many=True).dump(comments).data

    @staticmethod
    def select_comment(comment_id):
        comment = Comment.query. \
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
                Rating.down_vote,
                Rating.up_vote). \
            filter(Comment.comment_id == comment_id).first()
        return CommentsSchema(many=False).dump(comment).data

    @staticmethod
    def update_rating(rating_id, down_vote=None, up_vote=None, view=None):
        rating = Rating.query.filter(Rating.rating_id == rating_id).first()
        if down_vote:
            rating.down_vote += int(down_vote)
        if up_vote:
            rating.up_vote += int(up_vote)
        if view:
            rating.views += int(view)
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
        return new_forum_post.post_id, new_rating.rating_id

    @staticmethod
    def select_forum_posts(game_id, hours=8766, order=None, desending=True):
        """ Dynamically selecting forum posts based on passed parameters """
        today_datetime = datetime.utcnow()
        delta_time = today_datetime - timedelta(hours=int(hours))
        forum_posts = ForumPost.query. \
            join(Rating, ForumPost.rating_id == Rating.rating_id). \
            join(User, ForumPost.author_id == User.user_id). \
            add_columns(
                ForumPost.post_id,
                ForumPost.rating_id,
                ForumPost.game_id,
                ForumPost.author_id,
                ForumPost.post_description,
                ForumPost.date_posted,
                Rating.down_vote,
                Rating.up_vote,
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
                ForumPost.author_id,
                ForumPost.post_description,
                ForumPost.post_text,
                ForumPost.date_posted,
                Rating.down_vote,
                Rating.up_vote,
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
        add_associate_id.associated_id = new_build.build_id
        db.session.commit()
        return new_build.build_id, new_rating.rating_id

    @staticmethod
    def select_build(build_id):
        build = Build.query. \
            join(Rating, Build.rating_id == Rating.rating_id). \
            join(User, Build.author_id == User.user_id). \
            add_columns(
                Build.build_id,
                Build.rating_id,
                Build.author_id,
                Build.game_id,
                Build.build_description,
                Build.build_markup,
                Build.image_url,
                Build.date_posted,
                Rating.down_vote,
                Rating.up_vote,
                Rating.views,
                User.username). \
            filter(Build.build_id == build_id).first()
        return BuildRatingSchema(many=False).dump(build).data

    @staticmethod
    def select_builds(game_id, hours=8766, order=None, desending=True):
        today_datetime = datetime.utcnow()
        delta_time = today_datetime - timedelta(hours=int(hours))
        game_builds = Build.query. \
            join(Rating, Build.rating_id == Rating.rating_id). \
            join(User, Build.author_id == User.user_id). \
            add_columns(
                Build.build_id,
                Build.rating_id,
                Build.author_id,
                Build.game_id,
                Build.build_description,
                Build.build_markup,
                Build.image_url,
                Build.date_posted,
                Rating.down_vote,
                Rating.up_vote,
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
        return new_game.game_id

    @staticmethod
    def select_games():
        games = Game.query.all()
        return GameSchema(many=True).dump(games).data

    @staticmethod
    def select_game(game_id):
        game = Game.query.filter(Game.game_id == game_id).first()
        return GameSchema(many=False).dump(game).data

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


class DS3Queries:

    @staticmethod
    def insert_build(build_id, game_id, stat_description, item_description, stats_dict, item_list, tag_list):
        build = DS3Build(
            build_id=build_id,
            game_id=game_id,
            stat_description=stat_description,
            item_description=item_description)
        db.session.add(build)
        db.session.commit()
        stats = DS3StatAllocation(
            build=build,
            luck=stats_dict['luck'],
            faith=stats_dict['faith'],
            intelligence=stats_dict['intelligence'],
            dexterity=stats_dict['dexterity'],
            strength=stats_dict['strength'],
            vitality=stats_dict['vitality'],
            endurance=stats_dict['endurance'],
            attunement=stats_dict['attunement'],
            vigor=stats_dict['vigor'])
        db.session.add(stats)
        db.session.commit()
        for item_dict in item_list:
            item = DS3Item.query.filter(
                DS3Item.item_id == item_dict['item_id']).first()
            item.build_items.append(build)

        for tag_dict in tag_list:
            tag = DS3Tag.query.filter(
                DS3Tag.tag_id == tag_dict['tag_id']).first()
            tag.build_tags.append(build)

        db.session.commit()
        return stats.stat_allocation_id

    @staticmethod
    def select_build(build_id):
        build = DS3Build.query. \
            filter(DS3Build.build_id == build_id). \
            options(joinedload('stats'), joinedload(
                'items'), joinedload('tags')).first()
        return DS3BuildSchema(many=False).dump(build).data

    @staticmethod
    def update_build(build_id, stat_description=None, item_description=None):
        build = DS3Build.query.filter(DS3Build.build_id == build_id).first()
        if stat_description:
            build.stat_description = stat_description

        if item_description:
            build.item_description = item_description

        db.session.commit()

    @staticmethod
    def delete_build(build_id):
        DS3Build.query.filter(DS3Build.build_id == build_id).delete()
        db.session.commit()

    @staticmethod
    def insert_item_relationships(build_id, item_list):
        build = DS3Build.query.filter(DS3Build.build_id == build_id).first()
        for item_dict in item_list:
            item = DS3Item.query.filter(
                DS3Item.item_id == item_dict['item_id']).first()
            item.build_items.append(build)

        db.session.commit()

    @staticmethod
    def delete_item_relationships(build_id, item_list):
        build = DS3Build.query.filter(DS3Build.build_id == build_id).first()
        for item_dict in item_list:
            item = DS3Item.query.filter(
                DS3Item.item_id == item_dict['item_id']).first()
            item.build_items.remove(build)

        db.session.commit()

    @staticmethod
    def insert_tag_relationships(build_id, tag_list):
        build = DS3Build.query.filter(DS3Build.build_id == build_id).first()
        for tag_dict in tag_list:
            tag = DS3Tag.query.filter(
                DS3Tag.tag_id == tag_dict['tag_id']).first()
            tag.build_tags.append(build)

        db.session.commit()

    @staticmethod
    def delete_tag_relationships(build_id, tag_list):
        build = DS3Build.query.filter(DS3Build.build_id == build_id).first()
        for tag_dict in tag_list:
            tag = DS3Tag.query.filter(
                DS3Tag.tag_id == tag_dict['tag_id']).first()
            tag.build_tags.remove(build)

        db.session.commit()

    @staticmethod
    def update_stat_allocation(stat_allocation_id, stats_dict):
        stat_allocation = DS3StatAllocation.query. \
            filter(DS3StatAllocation.stat_allocation_id == stat_allocation_id). \
            first()
        stat_allocation.luck = stats_dict['luck']
        stat_allocation.faith = stats_dict['faith']
        stat_allocation.intelligence = stats_dict['intelligence']
        stat_allocation.dexterity = stats_dict['dexterity']
        stat_allocation.strength = stats_dict['strength']
        stat_allocation.vitality = stats_dict['vitality']
        stat_allocation.endurance = stats_dict['endurance']
        stat_allocation.attunement = stats_dict['attunement']
        stat_allocation.vigor = stats_dict['vigor']
        db.session.commit()


if __name__ == '__main__':
    # print Queries.select_forum_posts(game_id=1, hours=8766, order=None, desending=True)
    print Queries.select_subscription_list(6)
