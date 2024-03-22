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
from passlib.hash import pbkdf2_sha256  # Import hash function


api = Api(app, version='1.0', title='User API', description='CRUD operations for users')



user_fields = api.model('User', {
    'username': fields.String,
    'password': fields.String,
    'email': fields.String,
    'superkey': fields.String
})


@api.route('/users')
class UserAPI(Resource):
    @api.expect(user_fields, validate=True)  
    # @api.marshal_with(user_fields, code=201) 
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


@api.route('/verify')  # Define the verify endpoint
class VerifyUser(Resource):
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
            return {"message":"Something went wrong","status": 400}, 400
        except:
            return {'message': 'Invalid or expired token'}, 400
        

@api.route('/login')
class Login(Resource):
    def post(self):

        try:
            data = request.json
            user = User.query.filter_by(username=data['username']).first()
            token=user.token(aud='login')
            if user and user.verify_password(data['password']):
                token=user.token(aud='tologin',exp=60)
                return {"message":"login successful","status":200,'token':token},200 
            return {"message": "Invalid username or password"}, 401
        except Exception as e:
            return {"message": str(e)}, 500
        
    # def post(self):
    #     data = request.json
    #     user = User.query.filter_by(username=data['username']).first()
    #     if user and user.password == data['password']:
    #         return {'message': 'Login successful'}, 200
    #     return {'message': 'Invalid credentials'}, 400





# @api.route('/reset')
# class ResetPassword(Resource):
#     def post(self):
#         data = request.json
#         user = User.query.filter_by(email=data['email']).first()
#         if user:
#             token = user.token(aud='reset')
#             send_email(user.username, user.email, token)
#             return {'message': 'Reset link sent to your email'}, 200
#         return {'message': 'User not found'}, 404
#     def put(self):
#         data = request.json
#         token = data['token']
#         payload = decode_token(token)
#         user = User.query.filter_by(id=payload['sub']).first()
#         if user:
#             user.password = data['password']
#             db.session.commit()
#             return {'message': 'Password reset successful'}, 200
#         return {'message': 'Invalid token'}, 400

@api.route('/reset')
class ResetPassword(Resource):
    def post(self):
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if user:
            token = user.token(aud='reset')
            send_email(user.username, user.email, token)  # You need to define send_email
            return {'message': 'Reset link sent to your email'}, 200
        return {'message': 'User not found'}, 404

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