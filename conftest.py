import pytest
from flask_restful import Api
from core import create_app

from user import db as user_db
from user.models import User   

from books import db as book_db
from books.book_models import Book

from user.routes import UserAPI, UserdeleteAPI , VerifyUser , Login, ResetPassword, ForgetPassword
# from books.book_routes import BookAPI, BookdeleteAPI, GetBook, ValidateBooks, UpdateBooks
# from cart.cart_routes import CartAPI, CartdeleteAPI, GetCart, UpdateCart, DeleteCart

@pytest.fixture
def user_app():
    app = create_app()
    user_db.init_app('datab_users' , 'test')
    with app.app_context():
        user_db.create_all()
        
    api = Api(app)
    api.add_resource(UserAPI, '/users')
    api.add_resource(UserdeleteAPI, '/delete')
    api.add_resource(VerifyUser, '/verify')
    api.add_resource(Login, '/login')
    api.add_resource(ResetPassword, '/reset')
    api.add_resource(ForgetPassword, '/forget')
    yield app
    
    with app.app_context():
        user_db.drop_all() 
        
@pytest.fixture
def user_client(user_app):
    return user_app.test_client()   