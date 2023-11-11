"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

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
def show_form():
    """Form that allows user to create new users"""
    return render_template("create_user.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    """takes user's submitted form and creates new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["url"]
    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return render_template(f"{new_user.id}")
