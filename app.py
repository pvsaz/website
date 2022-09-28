# library imports
import os
import re
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    request,
    flash,
    session,
)
from flask_login import LoginManager

# file imports
from horoscope import Horoscope
from views import account_views, horoscope_views, blog_views
from database import db

# initialize app/database and define index route
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["SQLALCHEMY_DATABASE_URI"]
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


# starting login manager
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return account_views.User.query.get(int(user_id))


# blueprint registration of modular files
app.register_blueprint(account_views.account_management, url_prefix="")
app.register_blueprint(horoscope_views.pokemon_horoscope, url_prefix="")
app.register_blueprint(blog_views.blog, url_prefix="")

# run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))
