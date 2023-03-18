from marshmallow import Schema, fields, ValidationError, EXCLUDE, INCLUDE
from osemu.api import models

def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")

class UserSchema(Schema):
    id = fields.UUID(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    created_on = fields.DateTime(dump_only=True)

class CompanySchema(Schema):
    model = models.Company
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)

class ConsoleSchema(Schema):
    model = models.Console
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    company = fields.Nested(CompanySchema, unknown=EXCLUDE)
    release_date = fields.Date()
    end_date = fields.Date()
    short_description = fields.String()
    wiki_url = fields.String()
    image_url = fields.String()

class LanguageSchema(Schema):

    model = models.Language
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    emulators = fields.Nested('EmulatorsForLanguageSchema', many=True, unknown=EXCLUDE)

class LicenseSchema(Schema):
    model = models.License
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    url = fields.String()

class EmulatorNameSchema(Schema):
    model = models.Emulator
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    
class EmulatorSchema(Schema):
    model = models.Emulator
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True, validate=must_not_be_blank)
    git_url = fields.String()
    gh_stars = fields.Integer()
    gh_forks = fields.Integer()
    website_url = fields.String()
    image_url = fields.String()
    consoles = fields.Nested(ConsoleSchema, many=True, unknown=EXCLUDE)
    license = fields.Nested(LicenseSchema, unknown=EXCLUDE)
    short_description = fields.String()
    latest_update = fields.DateTime()
    release_date = fields.Date()
    language_amounts = fields.Nested('LanguagesForEmulatorSchema', many=True)

class LanguagesForEmulatorSchema(Schema):
    model = models.EmulatorLanguage
    id = fields.UUID(dump_only=True)
    language = fields.Nested(LanguageSchema, only=('id', 'name'), unknown=EXCLUDE)
    amount = fields.Float(required=True)

class EmulatorsForLanguageSchema(Schema):
    model = models.EmulatorLanguage
    id = fields.UUID(dump_only=True)
    emulator = fields.Nested(EmulatorNameSchema, only=('id', 'name'), unknown=EXCLUDE)
    amount = fields.Float(required=True)

class ErrorResponse(Schema):
    message = fields.String(required=True)