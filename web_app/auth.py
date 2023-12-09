from flask import Blueprint, render_template, request, flash, redirect, url_for
from web_app import db, front, mail
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from validate_email_address import validate_email
from flask_mail import Message
from datetime import datetime, timedelta
import secrets


# Reusable functions

# Email address validation
def is_valid_email(email):
  return validate_email(email)

# Password validation
def validate_password(password):
  special_characters = set('!@&?%*')

  if not (7 <= len(password) <= 15):
    return "Password must be between 7 and 15 characters"
  elif not any(char.isupper() for char in password):
    return "Password must contain at least one uppercase letter"
  elif not any(char.islower() for char in password):
    return "Password must contain at least one lowercase letter"
  elif not any(char in special_characters for char in password):
    return "Password must contain at least one special character (!@&?%*)"
  elif not any(char.isdigit() for char in password):
    return "Password must contain at least one digit"
  else:
    return None


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
    validation_outcome = validate_password(password1)

    if existing_user:
      flash("User already exist", category='error')
    elif not is_valid_email(email):
      flash("Email invalid, Please provide a valid email address", category='error')
    elif len(username) < 3:
      flash("Username must be greater than 2 characters", category='error')
    elif password1 != password2:
      flash("Passwords do not match", category='error')
    elif (validation_outcome):
      flash(validation_outcome, category='error')
      return render_template("signup.html", user=current_user)
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
      flash('Account Created!', category='success')
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user)
      return redirect(url_for('front.mynotes'))    
  return render_template("signup.html", user=current_user)

# Route to reset the username
@auth.route('/reset_username', methods=['POST'])
@login_required
def reset_username():
  new_username = request.form.get('reset_name')

  # validate username
  if len(new_username) < 3:
      flash("Username must be greater than 2 characters", category='error')

  current_user.username = new_username

  db.session.commit()
  flash('Username Reset Successful!', category='success')
  return render_template('profile.html', user=current_user)

# Route to reset the username
@auth.route('/reset_email', methods=['POST'])
@login_required
def reset_email():
  new_email = request.form.get('reset_email')

  # validate email address
  if not is_valid_email(new_email):
      flash("Email invalid, Please provide a valid email address", category='error')

  current_user.email = new_email

  db.session.commit()
  flash('Email Reset Successful!', category='success')
  return render_template('profile.html', user=current_user)

# Route to reset the password
@auth.route('/reset_password', methods=['POST'])
@login_required
def reset_password():

  current_password = request.form.get('current_pass')
  new_password1 = request.form.get('new_pass1')
  new_password2 = request.form.get('new_pass2')

  # validate the current password
  if not check_password_hash(current_user.password, current_password):
    flash('Incorrect current password. Password Not Reset', category='error')
    return render_template('profile.html', user=current_user)

  # validate the new password
  validation_outcome = validate_password(new_password1)
  if new_password1 != new_password2 or validation_outcome:
    flash(validation_outcome or "Passwords do not match", category='error')
  else:
    password=generate_password_hash(new_password1, method='pbkdf2:sha256')
    current_user.password = password

    db.session.commit()
    flash('Password Reset Successful!', category='success')
  return render_template('profile.html', user=current_user)

# Route for initiating password reset
@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
  if request.method == 'POST':
    email = request.form.get('forgot_pass')
    user = User.query.filter_by(email=email).first()

    if user:
      send_reset_email(user)
      flash('Password reset email sent. Check your emails', category='success')
      return redirect(url_for('auth.login'))
    else:
      flash('No user found with that email address', category='error')
  return render_template('login.html')

# route for resetting the password by token
@auth.route('/reset_password_tokenized/<token>', methods=['GET','POST'])
def reset_password_tokenized(token):
  user = User.query.filter_by(reset_token=token).first()

  if not user or user.reset_token_expiration < datetime.utcnow():
    flash('Invalid or expired reset token. Generate another token', category='error')
    return redirect(url_for('auth.login'))

  if request.method == 'POST':
    new_password = request.form.get('new_tokenised_password')
    new_password2 = request.form.get('new_tokenised_password2')

    # validate the new password
    validation_outcome = validate_password(new_password)
    if validation_outcome or new_password != new_password2:
      flash(validation_outcome or "Passwords do not match", category='error')
      return render_template('reset_password.html', token=token, user=user)

    # Update the password
    user.password = generate_password_hash(new_password, method='pbkdf2:sha256') 
    user.reset_token = None
    user.reset_token_expiration = None
    db.session.commit()
    flash('Password reset successful!', category='success')
    return redirect(url_for('auth.login'))
  return render_template('reset_password.html', token=token, user=None)



# generate a secure token
def generate_reset_token():
  return secrets.token_urlsafe(32)

# send a password reset email
def send_reset_email(user):
  token = generate_reset_token()
  user.reset_token = token
  user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
  db.session.commit()

  msg = Message('Password Reset', recipients=[user.email])
  msg.body = f"Click the link to reset your password: {url_for('auth.reset_password_tokenized', token=token, _external=True)}"
  mail.send(msg)