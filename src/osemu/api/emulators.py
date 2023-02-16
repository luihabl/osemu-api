from flask import Blueprint, jsonify, request
# from marshmallow import ValidationError
# from sqlalchemy.exc import IntegrityError

# from .models import Emulator
# from .schema import EmulatorSchema
# from ..extensions import db

emulators_bp = Blueprint('emulators', __name__, url_prefix='/emulators')

# def filter_wild(query, par_list, data):
#     for key in par_list:
#         if key in data:
#             val = data[key]
#             attr = getattr(Emulator, key)
#             query = query.where(attr.ilike(f'%{val}%'))
#     return query

# def filter_exact(query, par_list, data):
#     for key in par_list:
#         if key in data:
#             val = data[key]
#             attr = getattr(Emulator, key)
#             query = query.where(attr == val)
#     return query

# def all_as_list(q):
#     return [it for (it,) in q.all()]

# @emulators_bp.route('/', methods=['GET'])
# def get_emulators():
#     data = request.values.to_dict()

#     emulators = filter_wild(db.select(Emulator), 
#                           ['name'], data)
#     emulators = filter_exact(emulators, ['id'], data)
#     emulators = all_as_list(db.session.execute(emulators))

#     if len(emulators) == 1:
#         return EmulatorSchema().dump(emulators[0])
#     return EmulatorSchema(many=True).dump(emulators) 

# @emulators_bp.route('/<id>', methods=['GET'])
# def get_emulator_by_id(id):
#         emulator = db.get_or_404(Emulator, id)
#         return EmulatorSchema().dump(emulator)

# @emulators_bp.route('/', methods=['POST'])
# def add_emulator():

#     json_data = request.get_json()
#     if not json_data:
#         return {"message": "No input data provided"}, 400  

#     try:
#         if isinstance(json_data, list):
#             emulator = EmulatorSchema(load_instance=True, many=True).load(json_data)
#         elif isinstance(json_data, dict):
#             emulator = EmulatorSchema(load_instance=True, many=False).load(json_data)
#         else:
#             raise ValidationError

#     except ValidationError as err:
#         return err.messages, 422

#     try:
#         if isinstance(emulator, list):
#             db.session.add_all(emulator)
#         else:
#             db.session.add(emulator)
#         db.session.commit()
#     except IntegrityError as err:
#         return f'{err.orig}', 422

#     return f'Emulator added [{json_data}]'


# @emulators_bp.route('/<id>', methods=['PATCH', 'PUT'])
# def update_emulator(id):

#     emulator = db.get_or_404(Emulator, id)

#     json_data = request.get_json()
#     if not json_data:
#         return "No input data provided", 400  

#     partial = request.method == 'PATCH'
    
#     try:
#         new_entry = EmulatorSchema().load(json_data, partial=partial)
#     except ValidationError as err:
#         return err.messages, 422

#     new_entry['id'] = emulator.id
#     for k in new_entry.keys():
#         setattr(emulator, k, new_entry[k])
#     db.session.commit()

#     return "Entry updated successfuly."