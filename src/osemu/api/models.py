from ..extensions import db
from sqlalchemy.orm import validates
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Console(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)
    manufacturer = db.Column(db.String(255), nullable=False) 

    @validates('name')
    def validate_name(self, key, name):
        if len(name) <= 2:
            raise ValueError('Console name must have at least two characters.')
        return name 

    @validates('manufacturer')
    def validate_manufacturer(self, key, manufacturer):
        if len(manufacturer) <= 2:
            raise ValueError('Manufacturer name must have at least two characters.')
        return manufacturer 

    __table_args__ = (
        CheckConstraint('char_length(name) > 2',
                        name='name_min_length'),
        CheckConstraint('char_length(manufacturer) > 2',
                        name='manufacturer_min_length')
    )


class Emulator(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False, unique=True)  
    git_url = db.Column(db.String(255), nullable=True) 
