from flask import Blueprint, jsonify, request
from .models import Console
from ..extensions import db

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')

@consoles_bp.route('/', methods=['GET'])
def show_stuff():
    consoles = Console.query.all()
    cd = []
    for console in consoles:
        cd.append({
            'name': console.name,
            'manufacturer': console.manufacturer
        })

    return cd


@consoles_bp.route('/', methods=['POST'])
def add_stuff():

    data = request.get_json()

    name = data['name']
    manufacturer = data['manufacturer']

    console = Console(id=None, name=name, manufacturer=manufacturer)
    db.session.add(console)
    db.session.commit()
    return f'Console added [{console.name}]'