from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os

app = Flask(__name__)
app.secret_key = os.urandom(12)
engine = create_engine('sqlite:///app.db', echo=True)

from app import views, models, api
