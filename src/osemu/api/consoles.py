from flask import Blueprint, request
from flask.views import MethodView

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


class EntryAPI(MethodView):
    """
    API for `/group/<id>/` endpoints
    """

    def __init__(self, Model, Schema):
        self.Model = Model
        self.Schema = Schema
    
    def get(self, id):
        entry = db.get_or_404(self.Model, id)
        return self.Schema().dump(entry)


    def _update(self, id):

        entry = db.get_or_404(self.Model, id)

        json_data = request.get_json()
        if not json_data:
            return "No input data provided", 400  

        partial = request.method == 'PATCH'
        
        try:
            new_entry = self.Schema().load(json_data, partial=partial)
        except ValidationError as err:
            return err.messages, 422

        new_entry['id'] = entry.id
        for k in new_entry.keys():
            setattr(entry, k, new_entry[k])
        db.session.commit()

        return "Entry updated successfuly."    

    def patch(self, id):
        return self._update(id)

    def put(self, id):
        return self._update(id)


class GroupAPI(MethodView):
    """
    API for `/group/` endpoints
    """

    def __init__(self, Model, Schema, **kwargs):
        self.Model = Model
        self.Schema = Schema
        self.searchable_fields = []
        for name, field in self.Schema().fields.items():
            if not field.dump_only:
                self.searchable_fields.append(name)

    def get(self):
        data = request.values.to_dict()

        print(self.searchable_fields)
        entries = filter_wild(db.select(self.Model), 
                            self.searchable_fields, data)
        entries = filter_exact(entries, ['id'], data)
        entries = all_as_list(db.session.execute(entries))

        if len(entries) == 1:
            return self.Schema().dump(entries[0])
        return self.Schema(many=True).dump(entries) 

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400  

        try:
            if isinstance(json_data, list):
                entry_data = self.Schema(many=True).load(json_data)
                entry = [self.Model(**c) for c in entry_data]
            elif isinstance(json_data, dict):
                entry_data = self.Schema(many=False).load(json_data)
                entry = self.Model(**entry_data)
            else:
                raise ValidationError

        except ValidationError as err:
            return err.messages, 422

        try:
            if isinstance(entry, list):
                db.session.add_all(entry)
            else:
                db.session.add(entry)
            db.session.commit()
        except IntegrityError as err:
            return f'{err.orig}', 422

        return f'Entry added [{json_data}]'

consoles_bp.add_url_rule('/', view_func=GroupAPI.as_view('console-group', Console, ConsoleSchema))
consoles_bp.add_url_rule('/<id>', view_func=EntryAPI.as_view('console-entry', Console, ConsoleSchema))

# @consoles_bp.route('/', methods=['GET'])
# def get_consoles():
#     data = request.values.to_dict()

#     consoles = filter_wild(db.select(Console), 
#                           ['name', 'manufacturer'], data)
#     consoles = filter_exact(consoles, ['id'], data)
#     consoles = all_as_list(db.session.execute(consoles))

#     if len(consoles) == 1:
#         return ConsoleSchema().dump(consoles[0])
#     return ConsoleSchema(many=True).dump(consoles) 

# @consoles_bp.route('/<id>', methods=['GET'])
# def get_console_by_id(id):
#         console = db.get_or_404(Console, id)
#         return ConsoleSchema().dump(console)

# @consoles_bp.route('/', methods=['POST'])
# def add_console():

#     json_data = request.get_json()
#     if not json_data:
#         return {"message": "No input data provided"}, 400  

#     try:
#         if isinstance(json_data, list):
#             console_data = ConsoleSchema(many=True).load(json_data)
#             console = [Console(**c) for c in console_data]
#         elif isinstance(json_data, dict):
#             console_data = ConsoleSchema(many=False).load(json_data)
#             console = Console(**console_data)
#         else:
#             raise ValidationError

#     except ValidationError as err:
#         return err.messages, 422

#     try:
#         if isinstance(console, list):
#             db.session.add_all(console)
#         else:
#             db.session.add(console)
#         db.session.commit()
#     except IntegrityError as err:
#         return f'{err.orig}', 422

#     return f'Console added [{json_data}]'


# @consoles_bp.route('/<id>', methods=['PATCH', 'PUT'])
# def update_console(id):

#     console = db.get_or_404(Console, id)

#     json_data = request.get_json()
#     if not json_data:
#         return "No input data provided", 400  

#     partial = request.method == 'PATCH'
    
#     try:
#         new_entry = ConsoleSchema().load(json_data, partial=partial)
#     except ValidationError as err:
#         return err.messages, 422

#     new_entry['id'] = console.id
#     for k in new_entry.keys():
#         setattr(console, k, new_entry[k])
#     db.session.commit()

#     return "Entry updated successfuly."