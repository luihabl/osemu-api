from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import Console
from .schema import ConsoleSchema
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
def new_console():

    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400  

    try:
        console = ConsoleSchema(load_instance=True).load(json_data)
    except ValidationError as err:
        return err.messages, 422

    try:
        db.session.add(console)
        db.session.commit()
    except IntegrityError as err:
        # msg = f'{err.orig}: {err.orig.args[1]}'
        return f'{err.orig}', 422

    return f'Console added [{json_data}]'