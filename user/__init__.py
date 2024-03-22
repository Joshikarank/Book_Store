from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from core import create_app

app = create_app('datab_users')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)