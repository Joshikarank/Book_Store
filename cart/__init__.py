from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from core import create_app

app = create_app('cart')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
