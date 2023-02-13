from flask import Blueprint, jsonify
from .models import Console
from ..extensions import db

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')

@consoles_bp.route('/show')
def show_stuff():
    consoles = Console.query.all()
    cd = ['a']
    for console in consoles:
        cd.append({
            'name': console.name,
            'manufacturer': console.manufacturer
        })

    return cd


@consoles_bp.route('/add/<name>')
def add_stuff(name):
    console = Console(id=None, name=name, manufacturer='Sony')
    db.session.add(console)
    db.session.commit()
    return f'Console added [{console.name}]'