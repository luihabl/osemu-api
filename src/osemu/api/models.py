from osemu.extensions import db, login_manager
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

emu_console = db.Table('emu_console',
                       db.Column('emulator_id', db.UUID, db.ForeignKey('emulator.id')),
                       db.Column('console_id', db.UUID, db.ForeignKey('console.id'))
                    )


class Company(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    consoles = db.relationship('Console', back_populates='company')

    def __repr__(self):
        return f'<Company {self.name}>'


class Console(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    company_id = db.Column(db.UUID, db.ForeignKey('company.id'))
    company = db.relationship('Company', back_populates='consoles')
    release_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    short_description = db.Column(db.Text)
    wiki_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))

    def __repr__(self) -> str:
        return f'<Console {self.name}>'


class EmulatorLanguage(db.Model):

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    emulator_id = db.Column('emulator_id', db.UUID, db.ForeignKey('emulator.id'))
    language_id = db.Column('language_id', db.UUID, db.ForeignKey('language.id'))

    emulator = db.relationship('Emulator', back_populates='language_amounts')
    language = db.relationship('Language', back_populates='emulators')

    amount = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f'<{self.emulator.name} {self.language.name} {self.amount}>'


class Language(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)

    emulators = db.relationship('EmulatorLanguage', cascade="all,delete", back_populates='language')

    def __repr__(self) -> str:
        return f'<Language {self.name}>'

class License(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255))
    emulators = db.relationship('Emulator', back_populates='license')

    def __repr__(self) -> str:
        return f'<License {self.name}>'

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

    language_amounts = db.relationship('EmulatorLanguage', cascade="all,delete", back_populates='emulator')
    
    def __repr__(self) -> str:
        return f'<Emulator {self.name}>'