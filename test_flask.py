from unittest import TestCase

from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """ Test Case for User views """

    def setUp(self):
        """ Add sample users """

        User.query.delete()
        user_1 = User(first_name="Samantha", last_name="Wright", img_url="https://images.pexels.com/photos/9794338/pexels-photo-9794338.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260")
        user_2 = User(first_name="Avery", last_name="Lenox")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()
    
    def tearDown(self):
        """ Tear Down """

        db.session.rollback()
    
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Wright, Samantha",html)
            self.assertIn("Lenox, Avery",html)
    
    def test_add_user(self):
        with app.test_client() as client:
            new_user = {
                "firstName": "Wesley",
                "lastName": "Mitchell",
                "imageUrl": "https://images.pexels.com/photos/4923041/pexels-photo-4923041.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
            resp = client.post('/users/new', data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Wesley",html)
            self.assertIn("Mitchell",html)
        with app.test_client() as client:
            new_user = User.query.filter_by(first_name="Wesley").first()
            resp = client.get(f'/users/{new_user.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("https://images.pexels.com/photos/4923041/pexels-photo-4923041.jpeg",html)
    def test_edit_user(self):
        with app.test_client() as client:
            user_to_edit = User.query.filter_by(first_name="Samantha").one()
            edited_user = {
                "firstName": "Portia",
                "lastName": "Brooks",
                "imageUrl": "https://images.pexels.com/photos/3851893/pexels-photo-3851893.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260"
            }
            resp = client.post(f'/users/{user_to_edit.id}/edit', data=edited_user, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Portia",html)
            self.assertIn("Brooks",html)
            self.assertIn("https://images.pexels.com/photos/3851893/pexels-photo-3851893.jpeg",html)
    def test_delete_user(self):
        with app.test_client() as client:
            user_to_delete = User.query.filter_by(first_name="Samantha").one()
            resp = client.get(f'/users/{user_to_delete.id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertNotIn("Samantha",html)
            self.assertNotIn("Wright",html)
            self.assertNotIn("https://images.pexels.com/photos/9794338/pexels-photo-9794338.jpeg",html)
            
class PostViewsTestCase(TestCase):
    """ Test case for Post views """

    def setUp(self):
        """ Add sample users and posts """

        User.query.delete()
        user_1 = User(first_name="Samantha", last_name="Wright", img_url="https://images.pexels.com/photos/9794338/pexels-photo-9794338.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260")
        user_2 = User(first_name="Avery", last_name="Lenox")
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.commit()

        Post.query.delete()
        post_1 = Post(title="Hello, world!", content="This is a post.", creator=user_1.id)
        post_2 = Post(title="Test Post", content="A test", creator=user_2.id)
        post_3 = Post(title="Second Post for User 1", content="User 1's second post.", creator=user_1.id)
        db.session.add(post_1)
        db.session.add(post_2)
        db.session.add(post_3)
        db.session.commit()
    
    def tearDown(self):
        """ Tear Down """

        db.session.rollback()
    
    def test_add_post(self):
        with app.test_client() as client:
            new_post = {
                "title": "My favorite post",
                "content": "This post is great.",
            }
            resp = client.post('/users/1/posts/new', data=new_post, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("My favorite post",html)
        with app.test_client() as client:
            new_post = Post.query.filter_by(title="My favorite post").first()
            resp = client.get(f'/posts/{new_post.id}')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("This post is great.",html)
    
    def test_list_posts(self):
        with app.test_client() as client:
            user = User.query.filter_by(first_name="Samantha").one()
            resp = client.get(f"/users/{user.id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Hello, world!",html)
            self.assertIn("Second Post for User 1",html)

    def test_edit_post(self):
        with app.test_client() as client:
            post_to_edit = Post.query.filter_by(title="Hello, world!").one()
            edited_post = {
                "title": "Hello, earth!",
                "content": "This post has been edited.",
            }
            resp = client.post(f'/posts/{post_to_edit.id}/edit', data=edited_post, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertIn("Hello, earth!",html)
            self.assertIn("This post has been edited.",html)
    def test_delete_post(self):
        with app.test_client() as client:
            post_to_delete = Post.query.filter_by(title="Hello, world!").one()
            resp = client.get(f'/posts/{post_to_delete.id}/delete',follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code,200)
            self.assertNotIn("Hello, world!",html)