from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
  app = Flask(__name__)
  load_dotenv()
  app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


  from .front import front
  from .auth import auth

  app.register_blueprint(front, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')
  
  return app