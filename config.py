from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Grocery(db.Model):
    """Класс описывает таблицу базы данных"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Grocery {self.name}>'