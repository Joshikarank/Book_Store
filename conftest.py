import pytest
from flask_restful import Api
from core import create_app

from user import db as user_db
from user.models import User   

from books import db as book_db
from books.book_models import Book

from cart import db as cart_db
from cart.cart_models import Cart

from user.routes import UserAPI, UserdeleteAPI , VerifyUser , Login, ResetPassword, ForgetPassword
from books.book_routes import AddingBookApi, RetreivingBookApi , DeletingBookApi, UpdatingbookApi
from cart.cart_routes import CartApi, DeletingCart, ordercart,Cancelordercart

@pytest.fixture
def user_app():
    app = create_app('datab_users' , 'test')
    user_db.init_app(app)
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

@pytest.fixture
def cart_app():
    app = create_app('cart' , 'test')
    cart_db.init_app(app)
    with app.app_context():
        cart_db.create_all()
    api = Api(app)
    api.add_resource(CartApi, '/addcarts')
    api.add_resource(DeletingCart, '/deletecart')
    api.add_resource(ordercart, '/order')
    api.add_resource(Cancelordercart, '/cancelorder')
    
    
    yield app
    
    with app.app_context():
        cart_db.drop_all() 
        
@pytest.fixture
def cart_client(cart_app):
    return cart_app.test_client()









@pytest.fixture
def book_app():
    app = create_app('book_data' , 'test')
    book_db.init_app(app)
    with app.app_context():
        book_db.create_all()
    api = Api(app)
    api.add_resource(AddingBookApi, '/addbook')
    api.add_resource(RetreivingBookApi, '/getbook')
    api.add_resource(DeletingBookApi, '/deletebook')
    api.add_resource(UpdatingbookApi, '/updatebooks')
    yield app
    
    with app.app_context():
        book_db.drop_all() 
        
@pytest.fixture
def book_client(book_app):
    return book_app.test_client()   



@pytest.fixture
def token(user_client):
    register_data =  {
    "username": "johhn_doe",
    "password" : "@Joshi2002",
    "email": "johhn@example.com",
    "superkey": "54321"
    }
    user_client.post('/users', json=register_data , headers={"Content-type":"application/json"})
    
    login_data =  {
        "username" : "johhn_doe",
        "password" : "@Joshi2002",
    }
    login_response = user_client.post('/login', json=login_data , headers={"Content-type":"application/json"})
    token=login_response.json['token']
    return token

    