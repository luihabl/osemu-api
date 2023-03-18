from flask import Blueprint

from osemu.api.models import User
from osemu.api.schema import UserSchema
from osemu.extensions import db, login_manager

from flask import request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    return db.session.get(User, id)

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify(message="Unauthorized: this action requires a logged in user."), 401

def create_user(data):
    try:
        db.session.add(User(
            email=data['email'], 
            password=generate_password_hash(data['password'])
        ))
        db.session.commit()
        return True
    except:
        db.session.rollback()
        return False


def check_and_register_user(data):
    """Check if user exists and creates if not.

    Args:
        data (dict): dictionary with data, including email and password.

    Raises:
        ValueError: Raised if user already exists or if not possible to create.
    """    

    parsed = UserSchema().load(data)

    q = db.session.query(User).filter_by(email=parsed['email'])
    if q.count() > 0:
       raise ValueError('Email in use.')
    
    res = create_user(parsed)
    if not res:
        raise ValueError('Not able to create user')


@auth_bp.route('/signup', methods=['POST'])
@login_required
def signup():
    """Create a user.
    ---
    post:
      description: Create a user.
      tags:
        - Auth
      security:
        - cookieAuth: []
      requestBody:
        required: True
        content:
            application/json:
              schema: UserSchema
      responses:
        200:
          description: User created succesfully.
        400:
          description: Invalid data provided. This means the user already exists or the data is not formatted correctly.
      
    """

    # parse data
    data = request.get_json()
    if not data:
        return jsonify(message='No JSON provided.'), 400
    
    try:
        check_and_register_user(data)
        return jsonify(message='User created successfuly.'), 200
    except:
        return jsonify(message='Invalid information provided.'), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user.
    ---
    post:
      description: Login a user.
      tags:
        - Auth
      requestBody:
        required: True
        content:
            application/json:
              schema: UserSchema
      responses:
        200:
          description: Logged in succesfully.
        400:
          description: Invalid data provided. This means the user was not found or the data is not formatted correctly.
    """
    # parse data
    data = request.get_json()
    if not data:
        return jsonify(message='No JSON provided.'), 400

    try:
        parsed = UserSchema().load(data)
    except ValidationError:
        return jsonify(message='Invalid JSON provided.'), 400

    # check if user exists
    try:
        user = db.session.query(User).filter_by(email=parsed['email']).one()
    except (MultipleResultsFound, NoResultFound):
        return jsonify(message='Invalid information.'), 400

    # check password
    pwd_match = check_password_hash(user.password, parsed['password'])
    if not pwd_match:
        return jsonify(message='Invalid information.'), 400

    # login
    login_user(user)

    return jsonify(message='User logged in successfuly.'), 200
    

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Logout current user.
    ---
    post:
      description: Logout current user.
      tags:
        - Auth
      security:
        - cookieAuth: []
      responses:
        200:
          description: Logged out.
        401:
          description: Not logged in for logout.
    
    """
    logout_user()
    return jsonify(message='Logged out successfuly.')


@auth_bp.route('/user', methods=['GET'])
@login_required
def get_user():
    """Get current user information.
    ---
    get:
      description: Get current user information.
      tags:
        - Auth
      security:
        - cookieAuth: []
      responses:
        200:
          description: Get current user information.
          content:
            application/json:
              schema: UserSchema
        401:
          description: Unauthorized to get user info.
    """
    return jsonify(UserSchema().dump(current_user))