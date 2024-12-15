from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

"""Initialisation page set up"""
app.config['SECRET_KEY'] = 'My$ecur3Key@2024!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/noemifavilli/database/app.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

"""Creates tables"""
with app.app_context():
    db.create_all()