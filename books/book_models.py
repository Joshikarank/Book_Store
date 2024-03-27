from . import db
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

class Book(db.Model):
    __tablename__ = 'Books'
    book_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float,  nullable=False)   
    quantity = db.Column(db.Integer, nullable=False)
    userid = db.Column(db.Integer, nullable=False)
    
    @property
    def to_json(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'price': self.price,
            'quantity': self.quantity,
        }
