from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from os import path
# from dotenv import load_dotenv
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()

def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY']= my_key # my_key is an env variable

  app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{os.envoron["DB_USER"]}:{os.environ["DB_PASSWORD"]}@/'
    f'{os.environ["DB_NAME"]}?host=/cloudsql/{os.environ["CONNECTION_NAME"]}'
  )
  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 465
  app.config['MAIL_USE_TLS'] = False
  app.config['MAIL_USE_SSL'] = True
  app.config['MAIL_USERNAME'] = 'musaqwabe@gmail.com'
  with open('email_pass.txt', 'r') as f:
    app.config['MAIL_PASSWORD'] = f.read().strip()
  app.config['MAIL_DEFAULT_SENDER'] = 'musaqwabe@gmail.com'
  
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
