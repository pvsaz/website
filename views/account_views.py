from database import db
from .blog_views import BlogPost
from flask_login import login_user, UserMixin, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (
    Blueprint,
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    request,
    flash,
    session,
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return "Blog post " + str(self.id)


account_management = Blueprint(
    "account_management", __name__, template_folder="templates", static_folder="static"
)


@account_management.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    if user:
        flash("Username already exists, please login under Your Account.")
        return redirect(url_for("account_management.signup"))
    if username == "" or password == "":
        flash("Please enter both a username and a password.")
        return redirect(url_for("account_management.signup"))
    if len(username) > 100:
        flash("Username too long. Limit is 100 characters.")
        return redirect(url_for("account_management.signup"))
    if len(password) > 10:
        flash("Password too long. Limit is 10 characters.")
        return redirect(url_for("account_management.signup"))
    new_user = User(
        username=username, password=generate_password_hash(password, method="sha256")
    )

    db.session.add(new_user)
    db.session.commit()
    user = User.query.filter_by(username=username).first()
    login_user(user, remember=False)
    return redirect(url_for("account_management.profile"))


@account_management.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        if (
            request.form.get("submit_button")
            == "Delete account and all associated posts"
        ):
            posts = BlogPost.query.filter(
                BlogPost.username == current_user.username
            ).all()
            if posts:
                for post in posts:
                    db.session.delete(post)
            account = User.query.filter(User.username == current_user.username).first()
            db.session.delete(account)
            db.session.commit()
            return redirect("/")
    else:
        return render_template("profile.html", username=current_user.username)


@account_management.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("account_management.login"))
    login_user(user, remember=remember)
    return redirect(url_for("account_management.profile"))


@account_management.route("/login")
def login():
    return render_template("login.html")


@account_management.route("/signup")
def signup():
    return render_template("signup.html")


@account_management.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
