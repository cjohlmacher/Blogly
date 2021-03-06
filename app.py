from flask import Flask, request, render_template, redirect, flash, sessions
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, Post_Tag
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
    posts = user.posts
    return render_template('user.html',user=user,posts=posts)

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
    user_deleted = User.query.filter_by(id=user_id).first()
    db.session.delete(user_deleted)
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

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    user = User.query.get(user_id)
    all_tags = Tag.query.all()
    return render_template("new-post.html", user=user, tags=all_tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def submit_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tag_names = request.form.getlist('tags')
    new_post = Post(title=title, content=content, creator=user_id)
    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).first()
        new_post.post_tags.append(tag)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.all()
    return render_template('post-edit.html', post=post,tags=all_tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
    title = request.form["title"]
    content = request.form["content"]
    tag_names = request.form.getlist('tags')
    post = Post.query.get_or_404(post_id)
    post.title = title
    post.content = content
    post.post_tags = []
    for tag_name in tag_names:
        tag = Tag.query.filter_by(name=tag_name).one()
        post.post_tags.append(tag)
    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.created_by
    delete_post = Post.query.filter_by(id=post_id).one()
    db.session.delete(delete_post)
    db.session.commit()
    return redirect(f"/users/{user.id}")

@app.route('/tags')
def show_tags():
    all_tags = Tag.query.all()
    return render_template('tags.html',tags=all_tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag.html',tag=tag)

@app.route('/tags/new')
def show_new_tag_form():
    return render_template('tag-new.html')

@app.route('/tags/new', methods=['POST'])
def new_tag():
    tag_name = request.form['tag-name']
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(f'/tags/{new_tag.id}')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-edit.html',tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    tag_name = request.form["tag-name"]
    update_tag = Tag.query.get_or_404(tag_id)
    update_tag.name = tag_name
    db.session.add(update_tag)
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')