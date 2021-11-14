from models import User, Post, db
from app import app

#Create all tables
db.drop_all()
db.create_all()

#Empty table
User.query.delete()
Post.query.delete()

#Add users
user_1 = User(first_name="Alan", last_name="Alda")
user_2 = User(first_name="Joel", last_name="Burton")
user_3 = User(first_name="Jane", last_name="Smith")

#Add to session
for user in [user_1,user_2,user_3]:
    db.session.add(user)
db.session.commit()