from flask import Flask
from dotenv import load_dotenv
import os


def create_app(test_config=None):
  app = Flask(__name__)
  load_dotenv()

  app.secret_key = os.getenv('APP_SECRET')

  from . import urlshort
  app.register_blueprint(urlshort.bp)

  return app