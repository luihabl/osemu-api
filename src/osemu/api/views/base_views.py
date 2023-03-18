from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError, fields, EXCLUDE
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from osemu.api.schema import *
from uuid import UUID
import sys

from functools import wraps
from flask_login import current_user
from osemu.extensions import login_manager, db


def uuid_is_valid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False
    return str(uuid_obj) == uuid_to_test


def method_login_required():
    def _method_login_required(f):
        @wraps(f)
        def __method_login_required(*args, **kwargs):
            token = None
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            return f(*args, **kwargs)
        return __method_login_required
    return _method_login_required


def _all_as_list(q):
    return [it for (it,) in q.all()]

def _filter_wild(Model, query, par_list, data):
    for key in par_list:
        if key in data:
            val = data[key]
            attr = getattr(Model, key)
            query = query.where(attr.ilike(f'%{val}%'))
    return query

def _filter_exact(Model, query, par_list, data):
    for key in par_list:
        if key in data:
            val = data[key]
            attr = getattr(Model, key)
            query = query.where(attr == val)
    return query

from types import FunctionType

def _get_schema(Schema):
    if isinstance(Schema, FunctionType):
        Schema = Schema()
    elif isinstance(Schema, str):
        return getattr(sys.modules[__name__], Schema)
    else:
        return Schema

def _find_entry(Schema, raw_data):
    search_keys = {}

    Schema = _get_schema(Schema)

    for k, v in raw_data.items():
        col = Schema.model.__dict__[k]

        try:
            if col.primary_key or (not col.nullable and col.unique):
                search_keys[k] = v
        except AttributeError:
            continue
    
    if search_keys == {}:
        return None

    return db.session.query(Schema.model).filter_by(**search_keys).first()


def get_or_create_obj(Schema, data, add=False):
    """Find an object in database or create a new one. This function is called recursively.

    Args:
        Schema (Schema): Schema defined in schema.py
        data (dict): Dictionary used to create the objects
        add (bool, optional): Whether to add the object directly to the database or return the objects. Data is not commited. Defaults to False.

    Returns:
        Model: Found or created object.
    """

    Schema = _get_schema(Schema)

    if isinstance(data, list):
        entry_data = Schema(many=True).load(data)
        return [get_or_create_obj(Schema, c, add) for c in entry_data]
    elif isinstance(data, dict):

        # Tries to find obj, and if finds it, skips this part below and just returns object
        obj_found = _find_entry(Schema, data)
        if obj_found:
            return obj_found

        entry_data = Schema(many=False).load(data)

        input_data = {}

        for k, v in entry_data.items():
            field = Schema().fields[k]
            if not isinstance(field, fields.Nested):
                input_data[k] = v
            else:
                NestedSchema = field.nested
                is_many = field.many
                
                if is_many:
                    input_data[k] = [get_or_create_obj(NestedSchema, vi, add) for vi in v]
                else:
                    input_data[k] = get_or_create_obj(NestedSchema, v, add)

        obj = Schema().model(**input_data)
        if add:
            db.session.add_all([obj])

        return obj
    else:
        raise ValueError("Incorrect input data type")


def update_obj(Schema, obj, data):
    """Updates one or more object from a dictionary.

    Args:
        Schema (Schema): Object marshmallow schema
        obj (db.Model): Object to be updated
        data (dict): Data to update

    Raises:
        ValueError: data is malformed.
    """    

    if isinstance(data, list):
        for d, o in zip(data, obj):
            update_obj(Schema, o, d)
    elif isinstance(data, dict):

        for k, v in data.items():

            field = Schema().fields[k]

            if not isinstance(field, fields.Nested):
                setattr(obj, k, v)
            else:
                NestedSchema = field.nested
                is_many = field.many
                if is_many:
                    nested_list = [get_or_create_obj(NestedSchema, vi) for vi in v]
                    setattr(obj, k, nested_list)
                    update_obj(NestedSchema, nested_list, v)
                else:
                    nested = get_or_create_obj(NestedSchema, v)
                    setattr(obj, k, nested)
                    update_obj(NestedSchema, nested, v)

    else:
        raise ValueError("Incorrect input data type")


class BaseModelView(MethodView):
    """
    Base view for a model
    """
    def __init__(self, Model, Schema):
        self.Model = Model
        self.Schema = Schema

def get_entry_api_cls():
    """Returns the EntryAPI class. This is done to be able to change its docstring 
    in different places without changing other class definitions.

    Returns:
        EntryAPI: entry API class.
    """    

    class EntryAPI(BaseModelView):
        """
        API for `/group/<id>/` endpoints
        """
        
        def get(self, id):

            try:
                entry = db.session.get(self.Model, id)
                if not entry:
                    return jsonify(message="Entry not found.")
                return self.Schema().dump(entry)
            except:
                return jsonify(message="Impossible to fetch data, possibly a database server fault. Try again later."), 500
            
        def _update(self, id):
            
            try:
                entry = db.session.get(self.Model, id)
            except:
                return jsonify(message="Impossible to fetch data, possibly a database server fault. Try again later."), 500
            
            if not entry:
                return jsonify(message="Invalid data provided."), 400

            json_data = request.get_json()
            if not json_data:
                return jsonify(message="No input data provided"), 400  

            partial = request.method == 'PATCH'
            
            try:
                upd_data = self.Schema().load(json_data, partial=partial)
            except ValidationError as err:
                return jsonify(message=f'Invalid input data provided [{err.messages}]'), 400

            update_obj(self.Schema, entry, upd_data)

            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(message="Error on update."), 400

            return jsonify(message="Entry updated successfuly") , 200   

        @method_login_required()
        def patch(self, id):

            if not uuid_is_valid(id):
                return jsonify(message="Invalid id provided."), 400
            
            return self._update(id)

        @method_login_required()
        def put(self, id):

            if not uuid_is_valid(id):
                return jsonify(message="Invalid id provided."), 400
            
            return self._update(id)

        @method_login_required()
        def delete(self, id):

            if not uuid_is_valid(id):
                return jsonify(message="Invalid id provided."), 400
            
            try:
                entry = db.session.get(self.Model, id)
            except:
                return jsonify(message="Impossible to fetch data, possibly a database server fault. Try again later."), 500
            
            if not entry:
                return jsonify(message='Entry not found.')

            db.session.delete(entry)
            try:
                db.session.commit()
            except:
                db.session.rollback()
                return jsonify(message="Error on delete"), 400
            return jsonify(message="Entry deleted successfuly")
    
    return EntryAPI

def get_group_api_cls():
    """Returns the GroupAPI class. This is done to be able to change its docstring 
    in different places without changing other class definitions.

    Returns:
        GroupAPI: group API class.
    """    
        
    class GroupAPI(BaseModelView):
        """
        API for `/group/` endpoints
        """

        def __init__(self, Model, Schema, **kwargs):
            super().__init__(Model, Schema)
            self.searchable_fields = []
            for name, field in self.Schema().fields.items():
                if not field.dump_only:
                    self.searchable_fields.append(name)

        def get(self):
            data = request.values.to_dict()

            try:
                entries = _filter_wild(self.Model, db.select(self.Model), 
                                    self.searchable_fields, data)
                entries = _filter_exact(self.Model, entries, ['id'], data)
                entries = _all_as_list(db.session.execute(entries))
            except:
                return jsonify(message='Error when fetching data, possibly a database server fault. Try again later.'), 500

            if len(entries) == 1:
                return self.Schema().dump(entries[0])
            return self.Schema(many=True).dump(entries) 

        @method_login_required()
        def post(self):
            json_data = request.get_json()
            if not json_data:
                return jsonify(message="No input data provided."), 400  

            try:
                entry = get_or_create_obj(self.Schema, json_data)
            except ValidationError as err:
                return jsonify(message=f'Invalid input data provided [{err.messages}]'), 400
            except:
                return jsonify(message='Error when creating data, possibly a database server fault. Try again later.'), 500

            instances = {'existent':[], 'new': []}

            if not isinstance(entry, list):
                entry = [entry]
    
            for e in entry:
                if inspect(e).persistent:
                    instances['existent'].append(e)
                else:
                    instances['new'].append(e)

            try:
                db.session.add_all(instances['new'])
                db.session.commit()
            except IntegrityError as err:
                db.session.rollback()
                return jsonify(message=f'{err.orig}'), 500

            instances['new'] = self.Schema(many=True).dump(instances['new'])
            instances['existent'] = self.Schema(many=True).dump(instances['existent'])

            return jsonify(instances)
        
    return GroupAPI
