"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """redirects to /users"""
    return redirect("user_list")


@app.route("/user_list")
def list_users():
    """shows a list of all users"""
    users = User.query.all()
    return render_template("list_user.html", users=users)


@app.route("/create_user")
def show_create_form():
    """Form that allows user to create new users"""
    return render_template("create_user.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    """takes user's submitted form and creates new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["url"]
    if not image_url:
        image_url = None
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f"{new_user.id}")


@app.route("/<int:user_id>")
def show_user(user_id):
    """displays the selected user's profile"""
    user = User.query.get_or_404(user_id)
    return render_template("profile.html", user=user)


@app.route("/edit_user/<int:user_id>")
def show_edit_form(user_id):
    """displays form to edit a user"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)


@app.route("/edit_user", methods=["POST"])
def edit_user():
    """updates the user's info in the db to the given fields"""
    id = request.form["id"]
    user = User.query.get(id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["url"]
    db.session.commit()
    return redirect(f"{id}")


@app.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    """Removes the selected user from the database"""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/")


@app.route("/create_post/<int:user_id>")
def show_create_post_form(user_id):
    """displays form to create a post"""
    user = User.query.get_or_404(user_id)
    return render_template("create_post.html", user=user)


@app.route("/create_post/<user_id>", methods=["POST"])
def create_post(user_id):
    """creates a new post"""
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/{user_id}")


@app.route("/post/<int:post_id>")
def show_post(post_id):
    """Shows the selected post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)


@app.route("/edit_post/<int:post_id>")
def show_edit_post_form(post_id):
    """displays the form to edit the post"""
    post = Post.query.get_or_404(post_id)
    return render_template("edit_post.html", post=post)


@app.route("/edit_post/<int:post_id>", methods=["POST"])
def edit_post(post_id):
    """updates the post with the given fields"""
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    db.session.commit()
    return redirect(f"/post/{post_id}")


@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """deletes the post"""
    post = Post.query.get(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(f"/{user_id}")
