"""empty message

Revision ID: e5c0497f6f14
Revises: 
Create Date: 2018-11-25 18:33:01.981000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c0497f6f14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DS3_build',
    sa.Column('build_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('stat_description', sa.Text(), nullable=True),
    sa.Column('item_description', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('build_id')
    )
    op.create_table('DS3_item',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_table('DS3_tag',
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('tag_name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('tag_id')
    )
    op.create_table('build',
    sa.Column('build_id', sa.Integer(), nullable=False),
    sa.Column('build_description', sa.Text(), nullable=True),
    sa.Column('build_markup', sa.Text(), nullable=True),
    sa.Column('rating_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('image_url', sa.Text(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('build_id')
    )
    op.create_table('comment',
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('rating_id', sa.Integer(), nullable=True),
    sa.Column('associated_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('reply_id', sa.Integer(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('forum_post',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('rating_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('post_description', sa.Text(), nullable=True),
    sa.Column('post_text', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('game',
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('game_name', sa.String(length=128), nullable=True),
    sa.Column('game_description', sa.Text(), nullable=True),
    sa.Column('game_image', sa.Text(), nullable=True),
    sa.Column('game_table', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.create_table('rating',
    sa.Column('rating_id', sa.Integer(), nullable=False),
    sa.Column('associated_id', sa.Integer(), nullable=True),
    sa.Column('down_vote', sa.Integer(), nullable=True),
    sa.Column('up_vote', sa.Integer(), nullable=True),
    sa.Column('views', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('rating_id')
    )
    op.create_table('revoked_token',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=16), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=True),
    sa.Column('subscriber_count', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=16), nullable=True),
    sa.Column('user_level', sa.Integer(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('user_subscriptions',
    sa.Column('subscription_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('subscription_id')
    )
    op.create_table('DS3_item_relationships',
    sa.Column('build_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['build_id'], ['DS3_build.build_id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['DS3_item.item_id'], )
    )
    op.create_table('DS3_stat_allocation',
    sa.Column('stat_allocation_id', sa.Integer(), nullable=False),
    sa.Column('build_id', sa.Integer(), nullable=True),
    sa.Column('luck', sa.Integer(), nullable=True),
    sa.Column('faith', sa.Integer(), nullable=True),
    sa.Column('intelligence', sa.Integer(), nullable=True),
    sa.Column('dexterity', sa.Integer(), nullable=True),
    sa.Column('strength', sa.Integer(), nullable=True),
    sa.Column('vitality', sa.Integer(), nullable=True),
    sa.Column('endurance', sa.Integer(), nullable=True),
    sa.Column('attunement', sa.Integer(), nullable=True),
    sa.Column('vigor', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['build_id'], ['DS3_build.build_id'], ),
    sa.PrimaryKeyConstraint('stat_allocation_id'),
    sa.UniqueConstraint('build_id')
    )
    op.create_table('DS3_tag_relationships',
    sa.Column('build_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['build_id'], ['DS3_build.build_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['DS3_tag.tag_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('DS3_tag_relationships')
    op.drop_table('DS3_stat_allocation')
    op.drop_table('DS3_item_relationships')
    op.drop_table('user_subscriptions')
    op.drop_table('user')
    op.drop_table('revoked_token')
    op.drop_table('rating')
    op.drop_table('game')
    op.drop_table('forum_post')
    op.drop_table('comment')
    op.drop_table('build')
    op.drop_table('DS3_tag')
    op.drop_table('DS3_item')
    op.drop_table('DS3_build')
    # ### end Alembic commands ###
