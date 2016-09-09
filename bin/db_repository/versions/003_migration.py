from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('username', String),
    Column('password', String),
    Column('email', String),
    Column('registered_on', DateTime),
    Column('about_me', String),
    Column('last_seen', DateTime),
)

user = Table('user', post_meta,
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=20)),
    Column('password', String(length=10)),
    Column('email', String(length=50)),
    Column('registered_on', DateTime),
    Column('about_me', String(length=140)),
    Column('last_seen', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].drop()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].create()
    post_meta.tables['user'].drop()
