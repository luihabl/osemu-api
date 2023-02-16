from marshmallow import Schema, fields, ValidationError

def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")

class ConsoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    manufacturer = fields.String(required=True, validate=must_not_be_blank)

class EmulatorSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    git_url = fields.String(required=False)


