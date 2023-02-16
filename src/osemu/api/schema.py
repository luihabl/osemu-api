# from .models import Console, Emulator
# from ..extensions import ma

from marshmallow import Schema, fields, ValidationError

# Custom validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")

class ConsoleSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    manufacturer = fields.String(required=True, validate=must_not_be_blank)



# from marshmallow import fields

# class ConsoleSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Console


# class EmulatorSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Emulator
        
#     id = ma.auto_field()
#     name = ma.auto_field()
#     consoles = ma.auto_field()
