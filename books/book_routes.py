from books import app,db
from flask_restx import Api,Resource,fields
from books.book_schemas import BookValidator
from flask import request
from books.book_models import Book
from flask import g
from flask_jwt_extended.exceptions import JWTDecodeError
from books.utils import authorize_user

from flask import request



api=Api(app=app, title='Book Api',security='apiKey', doc="/docs")

@api.route('/addbook')
class AddingBookApi(Resource):
    method_decorators=[authorize_user]
    @api.doc(headers={"Authorization":"token for adding books"},body=api.model('adding book',{"title":fields.String(),"author":fields.String(),"price":fields.Integer(),"quantity":fields.Integer()}))
    def post(self):
        try:
            if not g.user['is_superuser']:
                return {"message": "Access denied! You cannot perform this operation", "status": 403}, 403
            data = request.json
            data['id']=g.user['id']
            serializer=BookValidator(**data)
            data=serializer.model_dump()
            book=Book(**data)
            db.session.add(book)
            db.session.commit()
            return {"message":"Book added successfully","data":book.to_json,"status":201},201
        except JWTDecodeError:
            return {"message":"Invalid Token","status":401},401
        except Exception as e:
            return {"message":str(e),"status code":400},400
       
    # @api.expect(api.model('retreiving book data',{'userid':fields.Integer()}))
@api.route('/getbook')
class RetreivingBookApi(Resource):

    @api.doc(headers={"Authorization":"token for retreiving book data"})
    def get(self,*args,**kwargs):
        try:
            books=Book.query.all()
            if not books:
                return {"message":"Book not found","status":400},400
            return {"msg":"retrieved successfully","data":[book.to_json for book in books]}
           
           
        except Exception as e:
            return {"message":str(e),"status":500},500
       
@api.route('/deletebook')
class DeletingBookApi(Resource):
    method_decorators=[authorize_user]
   
    @api.doc(headers={"Authorization":"token for deleting books"},body=api.model('deleting book',{"title":fields.String()}))
    def delete(self, *args, **kwargs):
        try:
            if not g.user['is_superuser']:
                return {"message": "Access denied! You cannot perform this operation", "status": 403}, 403
            data = request.json
            book_title = data.get('title')
            if not book_title:
                return {"message": "Book title is required to perform this operation", "status": 400}, 400
            book = Book.query.filter_by(title=book_title).first()
            if not book:
                return {"message": "Book not found", "status": 404}, 404
            db.session.delete(book)
            db.session.commit()
            return {"message": "Book deleted successfully", "status": 204}, 204
        except Exception as e:
            return {"message": str(e), "status": 500}, 500
       

   
@api.route('/updatebook')
class UpdatingbookApi(Resource):
    method_decorators=[authorize_user]
    @api.doc(headers={"Authorization":"token for updating books"},body=api.model('updating book',{"title":fields.String(),"author":fields.String(),"price":fields.Integer(),"quantity":fields.Integer()}))
    def put(self, *args, **kwargs):
        try:
            if not g.user['is_superuser']:
                return {"message": "Access denied! You cannot perform this operation", "status": 403}, 403
            data = request.json
            book_title = data.get('title')
            if not book_title:
                return {"message": "Book title is required to perform this operation", "status": 400}, 400
            book = Book.query.filter_by(title=book_title).first()
            if not book:
                return {"message": "Book not found", "status": 404}, 404
            [setattr(book, key, data.get(key, getattr(book, key))) for key in ['author', 'price', 'quantity']]
            db.session.commit()
            return {"message": "Book updated successfully", "status": 200}, 200
        except Exception as e:
            return {"message": str(e), "status": 500}, 500
       
# @api.route('/getBook')
# class getBookbyId(Resource):
#     @api.expect(api.model('getting book by id',{'id':fields.Integer()}))
#     def get(self,*args,**kwargs):
#         try:
           
#             book=Book.query.filter_by('id')
#             if not book:
#                 return {"message":"Book not found","status":400},400
#             return {"message":"Book fetched successfully","data":book.to_json,"status":200},200
#         except Exception as e:
#             return {"message":str(e),"status":400},400

@app.route('/getBook',methods=['GET'])
def get_book():
    bookid=request.args.get("book_id")
    if not bookid:
        return {"message":"Book not found","status":400},400
    book=Book.query.get(bookid)
    if not book:
        return {"message":"Invalid token","status":400},400
    return {"message":"User_id fetched successfully","data":book.to_json,'status':200},200
