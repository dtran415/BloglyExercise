"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    
    db.app = app
    app.app_context().push()
    db.init_app(app)

class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    
    posts = db.relationship('Post', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
class Post(db.Model):
    
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User')
    tags = db.relationship('Tag', secondary='posts_tags')
    
    @property
    def friendly_date(self):
        return self.created_at.strftime("%b %-d  %Y, %-I:%M %p")

class Tag(db.Model):
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    
    posts = db.relationship('Post', secondary='posts_tags')
    
class PostTag(db.Model):
    __tablename__ = "posts_tags"
    
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)