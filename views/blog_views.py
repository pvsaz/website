from database import db
from flask import Blueprint, render_template, request, redirect
from datetime import datetime
from flask_login import current_user


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    username = db.Column(db.String(100), unique=False)


blog = Blueprint("blog", __name__, template_folder="templates", static_folder="static")


@blog.route("/posts", methods=["GET", "POST"])
def posts():

    if request.method == "POST":
        post_title = request.form["title"]
        post_content = request.form["content"]
        post_username = current_user.username
        new_post = BlogPost(
            title=post_title, content=post_content, username=post_username
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect("/posts")
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template("posts.html", posts=all_posts)


@blog.route("/posts/delete/<int:id>")
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect("/posts")


@blog.route("/posts/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == "POST":

        post.title = request.form["title"]
        post.content = request.form["content"]
        db.session.commit()
        return redirect("/posts")
    else:
        return render_template("edit.html", post=post)
