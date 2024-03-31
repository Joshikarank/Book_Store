from flask import request
from flask_restx import Api, Resource,fields
from cart.cart_models import Cart, CartItems
from cart.utils import authorize_users
from flask import g
from cart import app, db
import requests as http
from cart.cart_schemas import Cart_validator
from jwt import DecodeError as JWTDecodeError
from user.routes import limiter

api=Api(app=app,title='Cart Api',security='apiKey',
        authorizations={
            'apiKey':{
                'type':'apiKey',
                'in':'header',
                'required':True,
                'name':'Authorization'
            }
        }, doc="/docs")

@api.route('/addcarts')
class CartApi(Resource):
    method_decorators = [authorize_users]
    @limiter.limit("20 per second")
    @api.doc(headers={"Authorization":"token for adding cart"},
                body=api.model("adding cart",{'bookid':fields.Integer(),'cart_item_quantity':fields.Integer()}))
    def post(self):
        try:
            serializer=Cart_validator(**request.json)
            data=serializer.model_dump()
            bookid=data['bookid']
            response=http.get(f'http://127.0.0.1:5000/getBook?book_id={bookid}')
            if response.status_code >= 400:
                return {"message": response.json()['message']}
            book_data=response.json()
            userid=g.user['id']
            cart=Cart.query.filter_by(userid=userid,is_ordered=False).first()
            if not cart:
                cart=Cart(userid=userid)
                db.session.add(cart)
                db.session.commit()
            price=book_data.get('price',0)
            cart_item = CartItems.query.filter_by(bookid=bookid,cart_item_id=cart.cart_id).first()
            if not cart_item:
                cart_item=CartItems(bookid=bookid, 
                                    cart_item_price=price, 
                                    cart_item_quantity=data['cart_item_quantity'],
                                    cartid=cart.cart_id)
                db.session.add(cart_item)
                db.session.commit()
            cart_item.cart_item_quantity=data['cart_item_quantity']
            cart_item.cart_item_price=book_data['data']['price']
            cart.cart_price = sum([item.cart_item_price * item.cart_item_quantity for item in cart.items])
            cart.cart_quantity = sum([item.cart_item_quantity for item in cart.items])
            db.session.commit()
            return {"message":"Cart created successfully","data":cart.to_json,"status":201},201
        except JWTDecodeError as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status":409},409
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status":500},500



@api.route('/deletecart')
class DeletingCart(Resource):
    method_decorators = [authorize_users]
    @limiter.limit("20 per second")
    @api.doc(headers={"Authorization":"token for deleting cart"},
                body=api.model('Deleting cart',{'cart_id':fields.Integer()}))
    def delete(self, *args, **kwargs):
        try:
            data=request.json
            cartid=data.get('cart_id')
            cart=Cart.query.filter_by(cart_id=cartid).first()
            cart_item=CartItems.query.filter_by(cartid=cartid).first()
            if not cart:
                return {"message":"cart not found","status":400},400
            db.session.delete(cart_item)
            db.session.delete(cart)
            db.session.commit()
            return {"message":"cart deleted successfully","status":204},204
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status":500},500

@api.route('/order')
class ordercart(Resource):
    method_decorators=[authorize_users]
    @limiter.limit("20 per second")
    @api.doc(headers={"Authorization":"token for ordering cart"})
    def post(self,*args,**kwargs):
        try:
            userid=g.user['id']
            cart=Cart.query.filter_by(userid=userid).first()
            if not cart:
                return {"message":"cart not found","status":404},404
            items=cart.items
            cart_data={}
            headers={'Content-Type': 'application/json'}
            for item in items:
                cart_data[item.bookid]=item.cart_item_quantity
            validate_response=http.post(f'http://127.0.0.1:5000/validatebooks',
                                        json=cart_data,headers=headers)
            if validate_response.status_code>=400:
                return {"message":"Unable to validate books","status":400},400
            order_response=http.patch(f'http://127.0.0.1:5000/updatebooks',
                                      json=cart_data,headers=headers)
            if order_response.status_code>=400:
                return {"message":"Unable to update books","status":400},400
            cart.is_ordered=True
            db.session.commit()
            return {"message":"cart ordered successfully","status":200},200
        except JWTDecodeError as e:
            return {"message":str(e),"status":400}
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status":500}
            

@api.route('/cancelorder')
class Cancelordercart(Resource):
    method_decorators=[authorize_users]
    @limiter.limit("20 per second")
    @api.doc(params={'id':'cart_id that should be cancelled'})
    def delete(self,*args,**kwargs):
        try:
            userid=g.user['id']
            id=request.args.get('id')
            cart=Cart.query.filter_by(userid=userid, is_ordered=True,cart_id=id).first()
            if not cart:
                return {"message":"cart not found","status":404},404
            items=cart.items
            cart_data={}
            headers={'Content-Type': 'application/json'}
            for item in items:
                cart_data[item.bookid]=-1*item.cart_item_quantity
            order_response=http.patch(f'http://127.0.0.1:5000/updatebooks',
                                      json=cart_data,headers=headers)
            if order_response.status_code>=400:
                return {"message":"Unable to update books","status":400},400
            for items in cart.items:
                db.session.delete(item)
                db.session.commit()
            db.session.delete(cart)
            db.session.commit()
            return {"message":"Order cancelled successfully","status":204},204
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status":500},500