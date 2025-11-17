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