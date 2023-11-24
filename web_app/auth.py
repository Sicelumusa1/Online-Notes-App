from flask import Blueprint, render_template, request, flash, redirect, url_for
from web_app import db, front
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash('Successfully logged in', category='success')
        login_user(user)
        return redirect(url_for('front.mynotes'))
      else:
        flash('Incorrect password', category='error')
    else:
      flash('User not registered, please signup it\'s free', category='error')
  return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  from web_app.front import front
  if request.method == "POST":
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
      flash("User already exist", category='error')
    elif len(email) < 4:
      flash("Email must be greater than 3 characters", category='error')
    elif len(username) < 2:
      flash("Email must be greater than 1 characters", category='error')
    elif password1 != password2:
      flash("Passwords do not match", category='error')
    elif len(password1) < 7:
      flash("Password must be greater than 6 characters", category='error')
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
      flash('Account Created!', category='success')
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user)
      return redirect(url_for('auth.login'))    
  return render_template("signup.html", user=current_user)

