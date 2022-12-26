from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin): # --> user mixin inheritance is only used where db user need to be logged in using flask_login frame
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # Create the relationship of the foreign key from Post.
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    # this posts will reference all of the posts that this user object in db has.
    # backref : access user from the post model obj. e.g post.username instead post.id to access username . read more i think
    # passive delete : see ondelete CASCADE

    comments = db.relationship('Comment', backref='user', passive_deletes=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    #  Foreign Key Relationship With User ID
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # even if the User in model is uppercase, in foreign key relation it is represented in lowercase.
    # ondelete CASCADE : when i delete the user, all the posts that the user being deleted is destroyed from the db.

    # End of Foreign Key Relationship
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    post_text = db.Column(db.String(10000), nullable=False)

    # Create the relationship of the foreign key from post
    comments = db.relationship('Comment', backref='post', passive_deletes=True)

# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key Relationship with User ID and Post ID

    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False) # even if the User in model is uppercase, in foreign key relation it is represented in lowercase.
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)

    # End of Foreign Key Relationship

    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    comment_text = db.Column(db.String(200), nullable=False)
