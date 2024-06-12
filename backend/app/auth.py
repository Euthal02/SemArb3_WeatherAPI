from apiflask import HTTPTokenAuth
from app.models.users import UsersModel

token_auth = HTTPTokenAuth()

@token_auth.verify_token
def verify_token( token ):
    user = UsersModel.verify_auth_token(token)
    if not user:
        return False
    return True

@token_auth.get_user_roles
def get_user_roles( user_auth_object ):
    current_user = UsersModel.verify_auth_token(user_auth_object.token)
    return UsersModel.get_roles(user=current_user)
