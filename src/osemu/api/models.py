from ..extensions import db
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid


emu_console = db.Table('emu_console',
                       db.Column('emulator_id', db.UUID, db.ForeignKey('emulator.id')),
                       db.Column('console_id', db.UUID, db.ForeignKey('console.id'))
                    )


class Company(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    consoles = db.relationship('Console', back_populates='company')


class Console(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    company_id = db.Column(db.UUID, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', back_populates='consoles')
    release_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    short_description = db.Column(db.Text)
    wiki_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))

    def __repr__(self) -> str:
        return f'Console(id={self.id}, name={self.name})'


class EmulatorLanguage(db.Model):
    __tablename__ = 'emulator_language'

    amount = db.Column(db.Float, nullable=False)

    emulator_id = db.Column(db.UUID, db.ForeignKey('emulator.id'), primary_key=True)
    language_id = db.Column(db.UUID, db.ForeignKey('language.id'), primary_key=True)
    
    emulator = db.relationship('Emulator', back_populates='languages')
    language = db.relationship('Language', back_populates='emulators')


class Language(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)

    emulators = db.relationship('EmulatorLanguage', back_populates='language')


class License(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255))
    emulators = db.relationship('Emulator', back_populates='license')


class Emulator(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)  
    git_url = db.Column(db.String(512))
    gh_stars = db.Column(db.Integer)
    website_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512)) 

    consoles = db.relationship('Console', secondary=emu_console, backref='emulators')

    license_id = db.Column(db.UUID, db.ForeignKey('license.id'))
    license = db.relationship('License', back_populates='emulators')

    short_description = db.Column(db.Text)
    latest_update = db.Column(db.DateTime)
    release_date = db.Column(db.Date)

    languages = db.relationship('EmulatorLanguage', back_populates='emulator')
    
    def __repr__(self) -> str:
        return f'Emulator(id={self.id}, name={self.name})'