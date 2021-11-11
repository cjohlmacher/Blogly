from flask_sqlalchemy import SQLAlchemy
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