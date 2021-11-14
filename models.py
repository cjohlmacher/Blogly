from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Needed to pip3 install IPython in the virutal environment to run from ipython.

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# MODELS GO HERE
class User(db.Model):
    """ User class """

    __tablename__ = "users"

    id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
    )
    first_name = db.Column(
        db.String(100),
        nullable=False
    )
    last_name = db.Column(
        db.String(100),
        nullable=True
    )
    img_url = db.Column(
        db.String,
        nullable=True,
        default="https://northaustinurology.com/app/uploads/2017/01/profile-silhouette.jpg"
    )

    def __repr__(self):
        user = self
        return f"<User id={user.id} first_name={user.first_name} last_name={user.last_name} img_url={user.img_url}"
    
    def get_full_name(self):
        user = self
        return f"{user.last_name}, {user.first_name}"
    
    # posts = db.relationship('Post', backref=db.backref("users", cascade="all, delete-orphan"))
    # posts = db.relationship('Post', backref="created_by", cascade="all, delete, delete-orphan")
    posts = db.relationship('Post', cascade="all,delete", backref="created_by")

class Post(db.Model):
    """ Posts class """

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    # creator = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        post = self
        return f"<Post id={post.id} title={post.title} content={post.content} creator={post.creator}>"
    
    