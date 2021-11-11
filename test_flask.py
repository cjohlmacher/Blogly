from unittest import TestCase

from app import app
from models import db, User

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
            self.assertEqual("one","one")
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
            


        
