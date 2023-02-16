from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from .models import Console
from .schema import ConsoleSchema
from ..extensions import db

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')

def filter_wild(query, par_list, data):
    for key in par_list:
        if key in data:
            val = data[key]
            attr = getattr(Console, key)
            query = query.where(attr.ilike(f'%{val}%'))
    return query

def filter_exact(query, par_list, data):
    for key in par_list:
        if key in data:
            val = data[key]
            attr = getattr(Console, key)
            query = query.where(attr == val)
    return query

def all_as_list(q):
    return [it for (it,) in q.all()]

@consoles_bp.route('/', methods=['GET'])
def get_consoles():
    data = request.values.to_dict()

    consoles = filter_wild(db.select(Console), 
                          ['name', 'manufacturer'], data)
    consoles = filter_exact(consoles, ['id'], data)
    consoles = all_as_list(db.session.execute(consoles))

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
        else:
            raise ValidationError

    except ValidationError as err:
        return err.messages, 422

    try:
        if isinstance(console, list):
            db.session.add_all(console)
        else:
            db.session.add(console)
        db.session.commit()
    except IntegrityError as err:
        return f'{err.orig}', 422

    return f'Console added [{json_data}]'


@consoles_bp.route('/<id>', methods=['GET'])
def get_console_by_id(id):
        console = db.get_or_404(Console, id)
        return ConsoleSchema().dump(console)


@consoles_bp.route('/<id>', methods=['PATCH', 'PUT'])
def update_console(id):

    console = db.get_or_404(Console, id)

    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400  

    partial = request.method == 'PATCH'
    
    try:
        new_entry = ConsoleSchema().load(json_data, partial=partial)
    except ValidationError as err:
        return err.messages, 422

    new_entry['id'] = console.id
    for k in new_entry.keys():
        setattr(console, k, new_entry[k])
    db.session.commit()

    return "Entry updated successfuly."