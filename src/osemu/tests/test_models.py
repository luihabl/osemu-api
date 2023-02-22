"""
Test data models
"""

import pytest
from unittest.mock import patch
from osemu.api.models import Console, Emulator
from osemu.api.schema import ConsoleSchema, EmulatorSchema
from osemu.api.base_views import _get_or_create_obj
from sqlalchemy.exc import IntegrityError


"""
Console tests
"""

def _add_to_db(_db, obj):
    if not isinstance(obj, list):
        obj = [obj]
    _db.session.add_all(obj)
    _db.session.commit()


def test_create_console(_db, app):

    data = {
        'name': 'Console 1',
        'manufacturer': 'Manufacturer 1'
    }

    parsed_data = ConsoleSchema().load(data)
    new_console = Console(**parsed_data)

    _db.session.add(new_console)
    _db.session.commit()

    q = _db.session.query(Console)

    assert q.count() == 1

    saved = q.first()

    assert saved.name == parsed_data['name']
    assert saved.manufacturer == parsed_data['manufacturer']

def test_create_many_console(_db, app):

    data = [
        {
            'name': 'Console 1',
            'manufacturer': 'Manufacturer 1'
        },
        {
            'name': 'Console 2',
            'manufacturer': 'Manufacturer 1'
        },
        {
            'name': 'Console 3',
            'manufacturer': 'Manufacturer 1'
        }
    ]

    parsed_data = ConsoleSchema(many=True).load(data)

    objs = [Console(**d) for d in parsed_data]

    _db.session.add_all(objs)
    _db.session.commit()

    q = _db.session.query(Console).all()

    assert len(q) == len(data)

    for dq, dd in zip(q, data):
        assert dq.name == dd['name']
        assert dq.manufacturer == dd['manufacturer']
        
    
def test_error_console_same_name(_db, app):
    
    data1 = {
        'name': 'Console 1',
        'manufacturer': 'Manufacturer 2'
    }

    _db.session.add(Console(**data1))
    _db.session.commit()

    data2 = {
        'name': 'Console 1',
        'manufacturer': 'Manufacturer 2'
    }

    with pytest.raises(IntegrityError):
        _db.session.add(Console(**data2))
        _db.session.commit()

    _db.session.rollback()
    q = _db.session.query(Console)
    assert q.count() == 1



"""
Emulator tests
"""

def test_create_emulator(_db, app):

    data = {
        'name': 'Emu 1',
        'consoles': []
    }

    parsed_data = EmulatorSchema().load(data)
    new_emu = Emulator(**parsed_data)

    _db.session.add(new_emu)
    _db.session.commit()

    q = _db.session.query(Emulator)

    assert q.count() == 1

    saved = q.first()

    assert saved.name == parsed_data['name']
    assert saved.consoles == parsed_data['consoles']

def test_create_many_emulators(_db, app):

    data = [
        {
            'name': 'Emu 1'
        },
        {
            'name': 'Emu 2'
        },
        {
            'name': 'Emu 3'
        }
    ]

    parsed_data = EmulatorSchema(many=True).load(data)

    objs = [Emulator(**d) for d in parsed_data]

    _db.session.add_all(objs)
    _db.session.commit()

    q = _db.session.query(Emulator).all()

    assert len(q) == len(data)

    for dq, dd in zip(q, data):
        assert dq.name == dd['name']
        
    
def test_error_emulator_same_name(_db, app):
    
    data1 = {
        'name': 'Emu 1'
    }

    _db.session.add(Emulator(**data1))
    _db.session.commit()

    data2 = {
        'name': 'Emu 1'
    }

    with pytest.raises(IntegrityError):
        _db.session.add(Emulator(**data2))
        _db.session.commit()

    _db.session.rollback()
    q = _db.session.query(Emulator)
    assert q.count() == 1

@patch('osemu.extensions.db')
def test_emulator_create_console_nested(mock_db, _db, app):
    mock_db = _db
    
    data = [
        {
            'name': 'Emu 1',
            'consoles': [
                {
                    'name': 'Console 1',
                    'manufacturer': 'Manufacturer 1'
                },
                {
                    'name': 'Console 2',
                    'manufacturer': 'Manufacturer 1'
                }
            ]
        },
        {
            'name': 'Emu 2',
            'consoles': [
                {
                    'name': 'Console 2',
                    'manufacturer': 'Manufacturer 1'
                },
                {
                    'name': 'Console 3',
                    'manufacturer': 'Manufacturer 1'
                }
            ]
        },
        {
            'name': 'Emu 3',
            'consoles': [
                {
                    'name': 'Console 1',
                    'manufacturer': 'Manufacturer 1'
                }
            ]
        }
    ]

    parsed_data = EmulatorSchema(many=True).load(data)

    _get_or_create_obj(EmulatorSchema, parsed_data, True)

    q = _db.session.query(Emulator).all()
    assert len(q) == len(parsed_data)

    q = _db.session.query(Console).all()
    assert len(q) == 3


