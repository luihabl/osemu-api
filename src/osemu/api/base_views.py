from flask import request, jsonify
from flask.views import MethodView
from marshmallow import ValidationError, fields, EXCLUDE
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.attributes import InstrumentedAttribute

from ..extensions import db

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

def _find_entry(Schema, raw_data):
    search_keys = {}
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


def _get_or_create_obj(Schema, data, add=False):
    """Find an object in database or create a new one. This function is called recursively.

    Args:
        Schema (Schema): Schema defined in schema.py
        data (dict): Dictionary used to create the objects
        add (bool, optional): Whether to add the object directly to the database or return the objects. Data is not commited. Defaults to False.

    Returns:
        Model: Found or created object.
    """    
    if isinstance(data, list):
        entry_data = Schema(many=True).load(data)
        return [_get_or_create_obj(Schema, c, add) for c in entry_data]
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
                    input_data[k] = [_get_or_create_obj(NestedSchema, vi, add) for vi in v]
                else:
                    input_data[k] = _get_or_create_obj(NestedSchema, v, add)

        obj = Schema.model(**input_data)
        if add:
            db.session.add_all([obj])

        return obj
    else:
        raise ValueError("Incorrect input data type")


def _update_obj(Schema, obj, data):
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
            _update_obj(Schema, o, d)
    elif isinstance(data, dict):

        for k, v in data.items():

            field = Schema().fields[k]

            if not isinstance(field, fields.Nested):
                setattr(obj, k, v)
            else:
                NestedSchema = field.nested
                is_many = field.many
                if is_many:
                    nested_list = [_get_or_create_obj(NestedSchema, vi) for vi in v]
                    setattr(obj, k, nested_list)
                    _update_obj(NestedSchema, nested_list, v)
                else:
                    nested = _get_or_create_obj(NestedSchema, v)
                    setattr(obj, k, nested)
                    _update_obj(NestedSchema, nested, v)

    else:
        raise ValueError("Incorrect input data type")


class BaseModelView(MethodView):
    """
    Base view for a model
    """
    def __init__(self, Model, Schema):
        self.Model = Model
        self.Schema = Schema


class EntryAPI(BaseModelView):
    """
    API for `/group/<id>/` endpoints
    """
    
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
            upd_data = self.Schema().load(json_data, partial=partial)
        except ValidationError as err:
            return err.messages, 400


        _update_obj(self.Schema, entry, upd_data)


        db.session.commit()

        return "Entry updated successfuly"    

    def patch(self, id):
        return self._update(id)

    def put(self, id):
        return self._update(id)


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

        entries = _filter_wild(self.Model, db.select(self.Model), 
                            self.searchable_fields, data)
        entries = _filter_exact(self.Model, entries, ['id'], data)
        entries = _all_as_list(db.session.execute(entries))

        if len(entries) == 1:
            return self.Schema().dump(entries[0])
        return self.Schema(many=True).dump(entries) 

    def post(self):
        json_data = request.get_json()
        if not json_data:
            return "No input data provided", 400  

        try:
            entry = _get_or_create_obj(self.Schema, json_data)
        except ValidationError as err:
            return err.messages, 400

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
            return f'{err.orig}', 400

        instances['new'] = self.Schema(many=True).dump(instances['new'])
        instances['existent'] = self.Schema(many=True).dump(instances['existent'])

        return jsonify(instances)
