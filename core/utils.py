import jwt
from flask_mail import Message
from . import mail  # Assuming this is where your Flask-Mail instance is created
from settings import settings

class JWT:
    key = settings.jwt_key
    algorithm = settings.jwt_algo

    @classmethod
    def encode(cls, user_dict):
        encoded = jwt.encode(user_dict, cls.key, algorithm=cls.algorithm)
        return encoded

    @classmethod
    def to_decode(cls, encoded, aud):
        decoded = jwt.decode(encoded, cls.key, algorithms=[cls.algorithm], audience=aud)
        return decoded

def send_email(username, email, token):
    msg = Message('Welcome to Book Store!',
                  sender=settings.mail_username,
                  recipients=[email])
    msg.body = f'''Hi {username},\n\n" \
        Welcome to Book Store! Please click the link below to verify your email address:\n\n \
        {settings.base_url}/verify?token={token}\n\n \
        Thanks for using Book Store. This verification is for security purposes.\n\n \
        Best regards,\n'''

    try:
        mail.send(msg)
        return "Email sent successfully!"
    except Exception as e:
        return str(e)
