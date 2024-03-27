from flask import request
from flask_restx import Api, Resource
from cart.cart_models import Cart, CartItems
from cart.utils import authorize_user
from flask import g
from cart import app, db
import requests

api = Api(app=app, title='Book Api', security='apiKey', doc="/docs")

@api.route('/addcarts')
class CartApi(Resource):
    method_decorators = [authorize_user]

    def post(self):
        try:
            data = request.json
            print(data)
            app.logger.info(f"Received data: {data}")  # Add logging for debugging
            if not data or 'book_id' not in data or 'quantity' not in data:
                return {"message": "Invalid request data", "status": 400}, 400
            book_id = data['book_id']
            quantity = data['quantity']

            response = requests.get(f'http://127.0.0.1:8000/getBook?book_id={book_id}')
            if response.status_code >= 400:
                return {"message": "Failed to fetch book data", "status": 400}, 400

            book = response.json()
            userid = g.user['id']

            cart = Cart.query.filter_by(userid=userid, is_ordered=False).first()
            if not cart:
                cart = Cart(userid=userid)
                db.session.add(cart)

            cart_item = CartItems.query.filter_by(cart_id=cart.cart_id, book_id=book_id).first()
            if not cart_item:
                cart_item = CartItems(cart_id=cart.cart_id, book_id=book_id, quantity=quantity, price=book['price'])
                db.session.add(cart_item)
            else:
                cart_item.quantity += quantity

            db.session.commit()

            return {"message": "Item added to cart", "status": 200}, 200

        except Exception as e:
            return {"message": "Internal Server Error", "status": 500}, 500