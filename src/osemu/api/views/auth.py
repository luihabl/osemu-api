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


@auth_bp.route('/signup', methods=['POST'])
def signup():

    # parse data
    data = request.get_json()
    if not data:
        return jsonify(message='No JSON provided.'), 400

    try:
        parsed = UserSchema().load(data)
    except ValidationError as err:
        return jsonify(message='Invalid JSON provided.'), 400


    # check if user exists
    q = db.session.query(User).filter_by(email=parsed['email'])
    if q.count() > 0:
        return jsonify(message='Email in use.'), 400

    # crate user
    if not create_user(parsed):
        return jsonify(message='Unable to create user.'), 400

    return jsonify(message='User created successfuly.'), 200


@auth_bp.route('/login', methods=['POST'])
def login():
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
    logout_user()
    return jsonify(message='Logged out successfuly.')


@auth_bp.route('/user', methods=['GET'])
@login_required
def get_user():
    return jsonify(UserSchema().dump(current_user))