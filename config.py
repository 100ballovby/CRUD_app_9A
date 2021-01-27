from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Grocery(db.Model):
    """Класс описывает базу данных"""
