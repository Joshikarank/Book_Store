from . import db
from passlib.hash import pbkdf2_sha256
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def __init__(self,username,email,password,**kwargs):
        self.username=username
        self.email=email
        self.password=pbkdf2_sha256.hash(password)
        self.__dict__.update(kwargs)

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)
    
    def token(self,aud='default', exp = 15):
        return create_access_token(identity=self.id, 
                                   additional_claims={'exp': datetime.utcnow()+timedelta(minutes=exp),
                                                      'aud': aud})
    
    @property
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_superuser': self.is_superuser,
            'is_verified': self.is_verified
        }
