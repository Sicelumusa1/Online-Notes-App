from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from os import path
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate

load_dotenv()

db = SQLAlchemy()
mail = Mail()
DB_NAME = 'notes_db'
db_pass = os.getenv('DB_KEY')

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY']= os.getenv('MYKEY')

  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') or \
    f'postgresql+psycopg2://postgres:{db_pass}@localhost/{DB_NAME}'
  
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  # (
  #   f'postgresql+psycopg2://{os.envoron["DB_USER"]}:{os.environ["DB_PASSWORD"]}@/'
  #   f'{os.environ["DB_NAME"]}?host=/cloudsql/{os.environ["CONNECTION_NAME"]}'
  # )
  app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
  app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
  app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
  app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
  app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
  app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')   
  app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
  
  db.init_app(app)
  mail.init_app(app)

  migrate = Migrate(app, db)

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
