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

    # @validates('name')
    # def validate_name(self, key, name):
    #     if len(name) <= 2:
    #         raise ValueError('Console name must have at least two characters.')
    #     return name 

    # @validates('company')
    # def validate_company(self, key, company):
    #     if len(company) <= 2:
    #         raise ValueError('company name must have at least two characters.')
    #     return company 

    # __table_args__ = (
    #     CheckConstraint('char_length(name) > 2',
    #                     name='name_min_length'),
    #     CheckConstraint('char_length(company) > 2',
    #                     name='company_min_length')
    # )
    def __repr__(self) -> str:
        return f'Console(id={self.id}, name={self.name})'


class ProgrammingLanguage(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)


class License(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False, unique=True)


class Emulator(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)  
    git_url = db.Column(db.String(255), nullable=True) 
    consoles = db.relationship('Console', secondary=emu_console, backref='emulators')

    def __repr__(self) -> str:
        return f'Emulator(id={self.id}, name={self.name})'