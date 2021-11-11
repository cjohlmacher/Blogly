from flask import Flask, request, render_template, redirect, flash, sessions
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'placeholder'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def redirect_to_users():
    return redirect('/users')

@app.route('/users')
def list_users():
    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('users.html',users=users)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user.html',user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html',user=user)

@app.route('/users/<int:user_id>/edit',methods=["POST"])
def update_user(user_id):
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    img_url = request.form["imageUrl"]
    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect("/users")

@app.route('/users/new')
def show_new_user_form():
    return render_template('new-user.html')

@app.route('/users/new',methods=["POST"])
def submit_user():
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    img_url = request.form["imageUrl"]
    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"/users/{new_user.id}")
