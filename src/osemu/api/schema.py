from marshmallow import Schema, fields, ValidationError, EXCLUDE
from .models import Console, Emulator

def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")

class ConsoleSchema(Schema):
    model = Console
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    company = fields.String(required=True, validate=must_not_be_blank)

class EmulatorSchema(Schema):
    model = Emulator
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    git_url = fields.String(required=False)
    consoles = fields.Nested(ConsoleSchema, many=True, unknown=EXCLUDE)


