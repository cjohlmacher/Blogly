from models import User, Post, Tag, Post_Tag, db
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

#Add posts
post_1 = Post(title="First Post", content="This is a post", creator=1)
post_2 = Post(title="Second Post", content="A wonderful post", creator=2)

#Add tags
tag_1 = Tag(name="fun")
tag_2 = Tag(name="sports")
tag_3 = Tag(name="TV")

#Add to session
for user in [user_1,user_2,user_3]:
    db.session.add(user)
for post in [post_1,post_2]:
    db.session.add(post)
for tag in [tag_1,tag_2,tag_3]:
    db.session.add(tag)
db.session.commit()