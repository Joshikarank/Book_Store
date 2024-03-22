from flask import Flask
from flask_jwt_extended import JWTManager
from settings import settings
from flask_mail import Mail, Message 

jwt= JWTManager()
mail = Mail()

def create_app(db_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:2002@localhost:5432/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = "12345"  # Change this to a strong secret key
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Example: Gmail SMTP server
    app.config['MAIL_PORT'] = 465  
    app.config['MAIL_USERNAME'] = 'joshikarank2002@gmail.com'  # Your email username
    app.config['MAIL_PASSWORD'] = 'zjwdzrdtfkeggibi'  # Your email password
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    jwt.init_app(app)
    mail.init_app(app)
    
    return app