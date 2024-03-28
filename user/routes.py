from flask import request
from . import db, app
from .models import User
from flask_restx import Api, Resource, fields
from .schemas import RegisterSerializer
from pydantic import ValidationError
from flask_jwt_extended import decode_token
from core.utils import send_email
from jwt import DecodeError as JWTDecodeError
from settings import settings
import jwt as JWT 
from passlib.hash import pbkdf2_sha256
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address



api=Api(app=app, title='Book Store Api',security='apiKey',
        authorizations={
            'apiKey':{
                'type':'apiKey',
                'in':'header',
                'required':True,
                'name':'Authorization'
            }
        }, 
        doc="/docs")
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day , 50 per hour"]
)


@api.route('/users')
class UserAPI(Resource):
    @limiter.limit("20 per second")
    @api.expect(api.model('signingin',{'username':fields.String(),'email':fields.String(),'password':fields.String(),'superkey':fields.String(required=False)}))
    def post(self):
        """Create a new user"""
        try:
            serializer = RegisterSerializer(**api.payload)
            data = serializer.model_dump()
            data['is_superuser'] = data.pop('superkey')
            user = User(**data)
            db.session.add(user)
            db.session.commit()
            token = user.token(aud='toVerify')
            
            
            send_email( user.username,user.email, token)
            return user.to_json, 201
        except ValidationError:
            return {'message': 'Validation Error on input data'}, 400

@api.route('/delete')
class UserdeleteAPI(Resource):
    @limiter.limit("20 per second")
    @api.expect(api.model('Deleting',{'username':fields.String(),'email':fields.String(),'password':fields.String()}))
    def delete(self):
        data=request.json
        try:
            serializer=RegisterSerializer(username=data['username'],password=data['password'],email=data['email'],superkey=data['superkey'])
            user=User.query.filter_by(username=data['username']).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return {"message":"User deleted successfully","status":204},204
            return {"message":"Username is incorrect","status":401},401
        except Exception as e:
            return {"message":str(e),"status":400},400

@api.route('/verify')  # Define the verify endpoint
class VerifyUser(Resource):
    @limiter.limit("20 per second")
    @api.expect(api.model('verifying',{'username':fields.String(),'email':fields.String(),'password':fields.String()}))
    def get(self):
        try:
            token = request.args.get('token')
            if not token:
                return {'msg': 'Token not found', 'status': 404}, 404
            payload = decode_token(token)
            user = User.query.filter_by(id=payload['sub']).first()
            if not user:
                return {'msg': 'User not found', 'status': 404}, 404
            user.is_verified = True
            db.session.commit()
            return {'message': 'User verified successfully', 'status': 200}, 200
        except JWTDecodeError:
            app.logger.exception(exc_info=False)
            return {"message":"Unable to decode token","status": 400}, 400
        except Exception:
            return {"message":"cant fetch data of user","status": 400}, 400
        except:
            return {'message': 'Invalid or expired token'}, 400
        

@api.route('/login')
class Login(Resource):
    @limiter.limit("20 per second")
    def post(self):

        try:
            data = request.json
            user = User.query.filter_by(username=data['username']).first()
            token = user.token(aud='login')
            if user and user.verify_password(data['password']) and token is not None:
                token = user.token(aud='tologin', exp=60)
                return {"message": "login successful", "status": 200, 'token': token}, 200
            return {"message": "Invalid username or password"}, 401
        except Exception as e:
            return {"message": str(e)}, 500
        

@api.route('/reset')
class ResetPassword(Resource):
    @limiter.limit("20 per second")
    @api.doc(params={"token":"token for reset password"},body=api.model('reset',{'new_password':fields.String()}))
    def put(self):
        data = request.json
        token = request.args.get('token')  # Get token from query parameters
        if not token:
            return {'message': 'Token is required in query parameters'}, 400

        payload = decode_token(token)
        user = User.query.filter_by(id=payload['sub']).first()
        if user:
            new_password = data.get('password')
            hashed_password = pbkdf2_sha256.hash(new_password)  # Hash the new password
            user.password = hashed_password
            db.session.commit()
            return {'message': 'Password reset successful'}, 200
        return {'message': 'Invalid token'}, 400
    

@api.route('/forgot')
class ForgetPassword(Resource):
    @limiter.limit("20 per second")
    @api.expect(api.model('forget',{"email":fields.String()}))
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user:
            token = user.token(aud='reset')
            send_email(user.username, user.email, token)  # You need to define send_email
            return {'message': 'Reset link sent to your email'}, 200
        return {'message': 'User not found'}, 404
    

@app.route('/getUser',methods=["GET"])
def get():
        user_id=request.args.get("user_id")
        if not id:
            return {"message":"User not found","status":400},400
        user=User.query.get(user_id)
        if not user:
            return {"message":"Invalid User","status":400},400
        return {"message":"User data fetched successfully","status":200, 'data': user.to_json},200