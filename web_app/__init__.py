from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from os import path
from dotenv import load_dotenv
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'notes_db'
load_dotenv()
my_key = os.getenv('MYKEY')

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY']= my_key

  app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{my_key}@localhost/{DB_NAME}'

  db.init_app(app)

  


  from web_app.front import front
  from web_app.auth import auth

  app.register_blueprint(front, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from web_app.models import User, Note

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app

def create_database(app):
  if not path.exists('web_app/'+ DB_NAME):
    with app.app_context():
      db.create_all()
      print('Database created')
