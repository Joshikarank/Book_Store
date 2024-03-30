from flask import request
from flask_jwt_extended.exceptions import JWTDecodeError
from flask_jwt_extended import decode_token
import requests as http
from flask import g


def authorize_users(function):
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return {'message': 'Token not found','status': 404}, 404
            payload = decode_token(token)
            response = http.get(f'http://127.0.0.1:7000/getUser?user_id={payload.get('sub')}')
            if response.status_code >= 400:
                return {"message":"cant fetch user data for cart","status":401}, 400
            user = response.json()['data']
            g.user = user
            if request.method in ['POST', 'PUT','PATCH']:
                request.json.update(userid=user['id'])
            else:
                kwargs.update(user_id=user['id'])
        except JWTDecodeError:
            return {'msg': 'Invalid Token','status': 401}, 401
        except Exception as e:
            return {'msg' : str(e), 'status' :500}
        return function(*args, **kwargs)
    wrapper.__name__ == function.__name__
                
    return wrapper