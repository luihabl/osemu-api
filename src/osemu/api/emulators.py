from flask import Blueprint

emulators_bp = Blueprint('emulators', __name__, url_prefix='/emulators')

@emulators_bp.route('/')
def show_stuff():
    return "Hey we are here!"


@emulators_bp.route('/<name>')
def show_stuff2(name):
    return f'Emu is {name}'