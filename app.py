import os
import re
from horoscope import *
from flask import Flask, render_template, request, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, UserMixin, current_user, login_required, logout_user





















app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text,nullable=False)
	date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
	email = db.Column(db.String(100), unique=False)
	
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))
	
	def __repr__(self):
		return 'Blog post ' + str(self.id)

@app.route('/')
def index():
	return render_template('index.html')






















# login endpoints

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

@app.route('/signup', methods=['POST'])
def signup_post():
	email = request.form.get('email')
	password = request.form.get('password')
	user = User.query.filter_by(email=email).first()
	if user: # if a user is found, we want to redirect back to signup page so user can try again
		flash('Email address already exists, please login under Your Account.')
		return redirect(url_for('signup'))
	if email == "" or password == "":
		flash('Please enter both an email address and a password.')
		return redirect(url_for('signup'))
	new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
	
	db.session.add(new_user)
	db.session.commit()
	
    # code to validate and add user to database goes here
	return redirect(url_for('profile'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
	if request.method == 'POST':
		if request.form.get('submit_button') == 'Delete account and all associated posts':
			posts = BlogPost.query.filter(BlogPost.email == current_user.email).all()
			if posts:
				for post in posts:
					db.session.delete(post)
			account = User.query.filter(User.email == current_user.email).first()
			db.session.delete(account)
			db.session.commit()
			return redirect('/')
	else:
		return render_template('profile.html', email=current_user.email)
	
@app.route('/login', methods=['POST'])
def login_post():
	email = request.form.get('email')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False
	user = User.query.filter_by(email=email).first()
	
	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('login'))
	login_user(user, remember=remember)
	return redirect(url_for('profile'))

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('index'))





















# posting and horoscope endpoints

@app.route('/pokemon/sign', methods=['GET','POST'])
def get_sign():
	if request.method == 'POST':
		star_sign = request.form['star_sign'].lower()
		user_horoscope = Horoscope(star_sign)
		return have_sign(user_horoscope)
	else:
		return render_template('horo.html')

@app.route('/pokemon/show')
def have_sign(user_horoscope):
	return render_template('showhoro.html', sign=user_horoscope.sign, horoscope=user_horoscope.horoscope,poke=user_horoscope.lucky_poke_name,pic=user_horoscope.lucky_poke_pic_url)
	
@app.route('/posts', methods = ['GET', 'POST'])
def posts():

	if request.method == 'POST':
		post_title = request.form['title']
		post_content = request.form['content']
		post_username = current_user.email
		new_post = BlogPost(title=post_title,content=post_content,email=post_username)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	else:
		all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
		return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
		post = BlogPost.query.get_or_404(id)
		db.session.delete(post)
		db.session.commit()
		return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
	post = BlogPost.query.get_or_404(id)
	if request.method == 'POST':
		
		post.title = request.form['title']
		post.content = request.form['content']
		db.session.commit()
		return redirect('/posts')
	else:
		return render_template('edit.html',post=post)






















if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))