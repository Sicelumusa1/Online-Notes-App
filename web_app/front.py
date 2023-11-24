from flask import Blueprint, render_template
from flask_login import login_required, current_user

front = Blueprint('front', __name__, template_folder='templates')

@front.route('/')
@front.route('/home')
def home():
  return render_template("home.html", user=None)

@front.route('/mynotes')
@login_required
def mynotes():
  return render_template("mynotes.html", user=current_user)