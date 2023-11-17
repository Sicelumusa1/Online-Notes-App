from flask import Blueprint, render_template

front = Blueprint('front', __name__)

@front.route('/')
def home():
  return render_template("home.html")