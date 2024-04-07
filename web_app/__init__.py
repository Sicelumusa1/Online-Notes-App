from flask import Flask
import os
import base64
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
conf_pass = os.getenv('MYKEY')
db_pass = os.getenv('DB_KEY')
email_pass = os.getenv('APP_EMAIL_PASS')

def create_app():
  app = Flask(__name__)
  encoded_secret_key = os.environ.get('my_key')
  if encoded_secret_key:
      decoded_secret_key = base64.b64decode(encoded_secret_key).decode('utf-8')
      app.config['SECRET_KEY'] = decoded_secret_key
  else:
    # Set a default secret key if 'my_key' is not present
    app.config['SECRET_KEY'] = 'default_secret_key'

  app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'postgresql+psycopg2://{os.environ["DB_USER"]}:{os.environ["DB_PASSWORD"]}'
        f'@{os.environ["DB_HOST"]}:{os.environ["DB_PORT"]}/{os.environ["DB_NAME"]}'
    )
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 465
  app.config['MAIL_USE_TLS'] = False
  app.config['MAIL_USE_SSL'] = True
  app.config['MAIL_USERNAME'] = 'musaqwabe@gmail.com'
  app.config['MAIL_PASSWORD'] = 'AveryGoodPassword'
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
    if not path.exists('web_app/' + os.environ["DB_NAME"]):
        with app.app_context():
            db.create_all()
            print('Database created')
