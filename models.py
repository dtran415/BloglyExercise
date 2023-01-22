"""Models for Blogly."""

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
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'