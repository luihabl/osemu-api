from flask import Blueprint

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')

@consoles_bp.route('/')
def show_stuff():
    return "Hey we are here!"


@consoles_bp.route('/<name>')
def show_stuff2(name):
    return f'Console is {name}'