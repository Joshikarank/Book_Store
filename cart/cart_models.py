from cart import db


class Cart(db.Model):
    __tablename__='carts'
    cart_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    cart_price=db.Column(db.Integer,nullable=False,default=0)
    cart_quantity=db.Column(db.Integer, nullable=False,default=0)
    is_ordered=db.Column(db.Boolean,default=False)
    ordered_at=db.Column(db.DateTime,nullable=True)
    userid=db.Column(db.Integer, nullable=False)
    Items=db.relationship('cartItems',back_populates='cart',lazy=True)
    
    @property
    def to_json(self):
        return {
            'cart_id':self.cart_id,
            'cart_price':self.cart_price,
            'cart_quantity':self.cart_quantity,
            'is_ordered':self.is_ordered,
            'ordered_at':self.ordered_at,
            'userid':self.userid
        }

class CartItems(db.Model):
        __tablename__='cartItems'
        cart_item_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
        cart_item_price=db.Column(db.Integer,nullable=False,default=0)
        cart_item_quantity=db.Column(db.Integer, nullable=False,default=0)
        bookid=db.Column(db.Integer, nullable=False)
        cartid=db.Column(db.Integer,db.ForeignKey('carts.cart_id',ondelete="CASCADE"),nullable=False)

        @property
        def to_json(self):
            return {
                'cart_item_id':self.cart_item_id,
                'cart_item_price':self.cart_item_price,
                'cart_item_quantity':self.cart_item_quantity
                
            }