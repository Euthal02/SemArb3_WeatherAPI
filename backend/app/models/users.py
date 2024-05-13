from apiflask import Schema
from apiflask.fields import String, Integer
from apiflask.validators import Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from app.extensions import db
from jwt import encode as jwt_encode
from jwt import decode as jwt_decode
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone

from app.extensions import db

# define the user table
class UsersModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(256))

    def __init__( self, email, name, password ):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in = 600):
        exp_timestamp = int(datetime.now(timezone.utc).timestamp()) + expires_in
        return jwt_encode(
            { 'id': self.id, 'exp': exp_timestamp },
            current_app.config['SECRET_KEY'], algorithm='HS256'
        )
    
    @staticmethod
    def verify_auth_token(token):
        try:
            data = jwt_decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return UsersModel.query.filter_by(id=data['id']).first()
        except ExpiredSignatureError:
            # Handle expired token, if necessary
            return None
        except InvalidTokenError:
            # Handle invalid token, if necessary
            return None
        except Exception as e:
            # Log or handle other exceptions
            print(f"An error occurred: {e}")
            return None

# define the schema for the user input
class UsersIn(Schema):
    name = String(required=True, validate=Length(0, 128))
    email = String(required=True, validate=[Length(0, 128), Email()])
    password = String(required=True, validate=Length(0, 256))

# define the schema for the output
class UsersOut(Schema):
    id = Integer()
    name = String()
    email = String()
    password = String()

class LoginIn(Schema):
    email = String(required=True, validate=[Length(0, 128), Email()])
    password = String(required=True, validate=Length(0, 256))

class TokenOut(Schema):
    token = String()
    duration = Integer() 
