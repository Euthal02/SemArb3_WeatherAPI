from app.users import bp 
from app.extensions import db
from werkzeug.security import generate_password_hash
from apiflask import abort as flask_abort
from app.auth import token_auth
from app.models.users import UsersModel, UsersIn, UsersOut, LoginIn, TokenOut
import logging

# get all users
@bp.get('/')
@bp.auth_required(token_auth)
@bp.output(UsersOut(many=True))
def view_users(database_table=UsersModel):
    return database_table.query.all()

# get user by id
@bp.get('/<int:user_id>')
@bp.auth_required(token_auth)
@bp.output(UsersOut)
def view_user_by_id(user_id, database_table=UsersModel):
    user = db.get_or_404(database_table, user_id)
    return user

# create new user
@bp.post('/create')
@bp.auth_required(token_auth)
@bp.input(UsersIn, location='json')
@bp.output(UsersOut, status_code=201)
def create_user(json_data, database_table=UsersModel):
    user = database_table(**json_data)
    db.session.add(user)
    db.session.commit()
    return user

# change the information for a db entry
@bp.patch('/<int:user_id>/edit')
@bp.auth_required(token_auth)
@bp.input(UsersIn(partial=True), location='json')
@bp.output(UsersOut)
def update_user(user_id, json_data, database_table=UsersModel):
    user = db.get_or_404(database_table, user_id)
    for key, value in json_data.items():
        insert_data = value
        if key == "password":
            insert_data = generate_password_hash(value)
        setattr(user, key, insert_data)
    db.session.commit()
    return user

# remove user by id
@bp.delete('/<int:user_id>/remove')
@bp.auth_required(token_auth)
@bp.output(UsersOut)
def delete_user(user_id, database_table=UsersModel):
    user = db.get_or_404(database_table, user_id)
    db.session.delete(user)
    db.session.commit()
    return user

# create new user
@bp.post('/login')
@bp.input(LoginIn, location='json')
@bp.output(TokenOut, status_code=201)
def login_user(json_data, database_table=UsersModel):
    # Find user by email
    user = database_table.query.filter_by(email=json_data.get('email')).first()
    # If user doesn't exist or password is wrong
    if not user or not user.check_password(json_data.get('password')):
        logging.warning('Unsuccessful login attempt from user: '+json_data.get('email'))
        flask_abort(401, "Invalid User or Password!")
    
    token = user.generate_auth_token(600)
    logging.info('User '+json_data.get('email') + ' logged in')
    return { 'token': token, 'duration': 600 }
