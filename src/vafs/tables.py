import sqlalchemy as sa
from sqlalchemy import select, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import create_view

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.Text, unique=True)
    username = sa.Column(sa.Text)
    password_hash = sa.Column(sa.Text)
    group = sa.Column(sa.Text)

class Event(Base):
    __tablename__ = 'events'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    title = sa.Column(sa.Text)
    date = sa.Column(sa.Text)

class Note(Base):
    __tablename__ = 'notes'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    title = sa.Column(sa.Text)
    description = sa.Column(sa.Text)