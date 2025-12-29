import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from eralchemy2 import render_er

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    firstname = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers = relationship(
        "Follower", foreign_keys="[Follower.user_to_id]", back_populates="user_to")
    following = relationship(
        "Follower", foreign_keys="[Follower.user_from_id]", back_populates="user_from")


class Follower(db.Model):
    __tablename__ = 'follower'

    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user_from = relationship("User", foreign_keys=[
                             user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[
                           user_to_id], back_populates="followers")


class Post(db.Model):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    user = relationship("User", back_populates="posts")
    media = relationship("Media", back_populates="post")
    comments = relationship("Comment", back_populates="post")


class Media(db.Model):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    post = relationship("Post", back_populates="media")


class Comment(db.Model):
    __tablename__ = 'comment'

    id = Column(Integer, primary_key=True)
    comment_text = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)

    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


if __name__ == '__main__':
    render_er(db.Model, 'diagram.png')
