from flask import request
from flask.views import MethodView
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from ..extensions import db

def all_as_list(q):
    return [it for (it,) in q.all()]

class BaseModelView(MethodView):
    """
    Base view for a model
    """
    def __init__(self, Model, Schema):
        self.Model = Model
        self.Schema = Schema

    def _filter_wild(self, query, par_list, data):
        for key in par_list:
            if key in data:
                val = data[key]
                attr = getattr(self.Model, key)
                query = query.where(attr.ilike(f'%{val}%'))
        return query

    def _filter_exact(self, query, par_list, data):
        for key in par_list:
            if key in data:
                val = data[key]
                attr = getattr(self.Model, key)
                query = query.where(attr == val)
        return query


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

        print(self.searchable_fields)
        entries = self._filter_wild(db.select(self.Model), 
                            self.searchable_fields, data)
        entries = self._filter_exact(entries, ['id'], data)
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
