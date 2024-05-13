from apiflask import HTTPTokenAuth
from app.models.users import UsersModel

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token(token):
    user = UsersModel.verify_auth_token(token)
    if not user:
        return False
    return True
