from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from .models import Console
from .schema import ConsoleSchema
from ..extensions import db

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')

def filter_wild(query, par_list, data):
    for key in par_list:
        if key in data:
            val = data[key]
            attr = getattr(Console, key)
            query = query.filter(attr.ilike(f'%{val}%'))
    return query

def filter_exact(query, par_list, data):
    for key in par_list:
        if key in data:
            val = data[key]
            attr = getattr(Console, key)
            query = query.filter(attr == val)
    return query

@consoles_bp.route('/', methods=['GET'])
def get_consoles():
    data = request.values.to_dict()

    consoles = filter_wild(db.session.query(Console), 
                          ['name', 'manufacturer'], data)
    consoles = filter_exact(consoles, ['id'], data)
    consoles = consoles.all()

    if len(consoles) == 1:
        return ConsoleSchema().dump(consoles[0])
    return ConsoleSchema(many=True).dump(consoles) 

@consoles_bp.route('/', methods=['POST'])
def add_console():

    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400  

    try:
        if isinstance(json_data, list):
            console = ConsoleSchema(load_instance=True, many=True).load(json_data)
        elif isinstance(json_data, dict):
            console = ConsoleSchema(load_instance=True, many=False).load(json_data)

    except ValidationError as err:
        return err.messages, 422

    try:
        db.session.add(console)
        db.session.commit()
    except IntegrityError as err:
        # msg = f'{err.orig}: {err.orig.args[1]}'
        return f'{err.orig}', 422

    return f'Console added [{json_data}]'