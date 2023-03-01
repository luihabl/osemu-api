"""
Test data models
"""

import pytest
from unittest.mock import patch
from osemu.api import models
from osemu.api.schema import ConsoleSchema, EmulatorSchema
from osemu.api.views.base_views import get_or_create_obj
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
        'company': {'name': 'company 1'}
    }

    parsed_data = ConsoleSchema().load(data)
    new_console = get_or_create_obj(ConsoleSchema, parsed_data)

    _db.session.add(new_console)
    _db.session.commit()

    q = _db.session.query(models.Console)
    assert q.count() == 1

    saved = q.first()

    assert saved.name == parsed_data['name']
    assert saved.company.name == parsed_data['company']['name']

    q = _db.session.query(models.Company)
    assert q.count() == 1

def test_create_many_console(_db, app):

    data = [
        {
            'name': 'Console 1',
            'company': {'name': 'company 1'}
        },
        {
            'name': 'Console 2',
            'company': {'name': 'company 2'}
        },
        {
            'name': 'Console 3',
            'company': {'name': 'company 3'}
        }
    ]

    parsed_data = ConsoleSchema(many=True).load(data)
    objs = get_or_create_obj(ConsoleSchema, parsed_data)

    _db.session.add_all(objs)
    _db.session.commit()

    q = _db.session.query(models.Console).all()

    assert len(q) == len(data)

    for dq, dd in zip(q, data):
        assert dq.name == dd['name']
        assert dq.company.name == dd['company']['name']
        
    
def test_error_console_same_name(_db, app):
    
    data1 = {
        'name': 'Console 1',
        'company': {'name': 'company 2'}
    }

    _db.session.add(get_or_create_obj(ConsoleSchema, data1))
    _db.session.commit()

    data2 = {
        'name': 'Console 1',
        'company': models.Company(name='company 2')
    }

    with pytest.raises(IntegrityError):
        _db.session.add(models.Console(**data2))
        _db.session.commit()

    _db.session.rollback()
    q = _db.session.query(models.Console)
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
    new_emu = models.Emulator(**parsed_data)

    _db.session.add(new_emu)
    _db.session.commit()

    q = _db.session.query(models.Emulator)

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

    objs = [models.Emulator(**d) for d in parsed_data]

    _db.session.add_all(objs)
    _db.session.commit()

    q = _db.session.query(models.Emulator).all()

    assert len(q) == len(data)

    for dq, dd in zip(q, data):
        assert dq.name == dd['name']
        
    
def test_error_emulator_same_name(_db, app):
    
    data1 = {
        'name': 'Emu 1'
    }

    _db.session.add(models.Emulator(**data1))
    _db.session.commit()

    data2 = {
        'name': 'Emu 1'
    }

    with pytest.raises(IntegrityError):
        _db.session.add(models.Emulator(**data2))
        _db.session.commit()

    _db.session.rollback()
    q = _db.session.query(models.Emulator)
    assert q.count() == 1


def test_emulator_language_create(_db, app):

    emu = models.Emulator(name='Emu 1')
   
    _db.session.add_all([emu])
    _db.session.commit()

    emu_entry = _db.session.query(models.Emulator).filter_by(name=emu.name).first()

    emu_lang = models.EmulatorLanguage(
        emulator=emu_entry, 
        language=models.Language(name='C++'),
        amount=0.8
    )

    _db.session.add_all([emu_lang])
    _db.session.commit()
    
    emu_entry = _db.session.query(models.Emulator).filter_by(name=emu.name).first()
    
    assert emu_entry.name == emu.name
    assert emu_entry.language_amounts[0].language.name == emu_lang.language.name
    assert emu_entry.language_amounts[0].amount == emu_lang.amount

    emu2 = models.Emulator(
        name='Emu 2',
        language_amounts=[
            models.EmulatorLanguage(
                language=models.Language(name='Python'),
                amount=0.8
            )
        ]
    )

    _db.session.add_all([emu2])
    _db.session.commit()
    
    emu2_entry = _db.session.query(models.Emulator).filter_by(name=emu2.name).first()
    
    assert emu2_entry.name == emu2.name
    assert emu2_entry.language_amounts[0].language.name == 'Python'

    python_lang = _db.session.query(models.Language).filter_by(name='Python').first()
    cpp_lang = _db.session.query(models.Language).filter_by(name='C++').first()

    emu3 = models.Emulator(
        name='Emu 3',
        language_amounts=[
            models.EmulatorLanguage(
                language=python_lang,
                amount=0.2
            ),
            models.EmulatorLanguage(
                language=cpp_lang,
                amount=0.8
            )
        ]
    )

    _db.session.add_all([emu3])
    _db.session.commit()
    
    emu3_entry = _db.session.query(models.Emulator).filter_by(name=emu3.name).first()
    
    assert emu3_entry.name == emu3.name
    assert emu3_entry.language_amounts[0].language.name == 'Python'
    assert emu3_entry.language_amounts[1].language.name == 'C++'

def test_emu_lang_create_from_dict(_db, app):
    data = {
        'name': 'Emu 1',
        'language_amounts': [
            {'language': {'name': 'Python'}, 'amount': 0.8},
            {'language': {'name': 'Go'}, 'amount': 0.2}
        ]
    }

    obj = get_or_create_obj(EmulatorSchema, data)
    
    _db.session.add_all([obj])
    _db.session.commit()

    db_obj = _db.session.query(models.Emulator).filter_by(name=data['name']).first()
    
    assert db_obj.name == data['name']
    assert db_obj.language_amounts[0].language.name == 'Python'
    assert db_obj.language_amounts[1].language.name == 'Go'

    data2 = {
        'name': 'Emu 2',
        'language_amounts': [
            {'language': {'name': 'C++'}, 'amount': 0.1},
            {'language': {'name': 'Go'}, 'amount': 0.9}
        ]
    }
    
    obj = get_or_create_obj(EmulatorSchema, data2)
    
    _db.session.add_all([obj])
    _db.session.commit()

    db_obj = _db.session.query(models.Emulator).filter_by(name=data2['name']).first()
    
    assert db_obj.name == data2['name']
    assert db_obj.language_amounts[0].language.name == 'C++'
    assert db_obj.language_amounts[1].language.name == 'Go'

    q = _db.session.query(models.Language).all()
    assert len(q) == 3

    q = _db.session.query(models.EmulatorLanguage).all()
    assert len(q) == 4


def test_create_delete_emu_lang_nested(app, _db):
    data = {
        'name': 'Emu 1',
        'language_amounts': [
            {'language': {'name': 'Python'}, 'amount': 0.8},
            {'language': {'name': 'Go'}, 'amount': 0.2}
        ]
    }

    obj = get_or_create_obj(EmulatorSchema, data)
    
    _db.session.add_all([obj])
    _db.session.commit()

    db_obj = _db.session.query(models.Emulator).filter_by(name=data['name']).first()
    
    assert db_obj.name == data['name']
    assert db_obj.language_amounts[0].language.name == 'Python'
    assert db_obj.language_amounts[1].language.name == 'Go'

    obj = _db.session.query(models.Language).filter_by(name='Python').first()
    _db.session.delete(obj)
    _db.session.commit()
    
    q = _db.session.query(models.Language).all()
    assert len(q) == 1

    db_obj = _db.session.query(models.Emulator).filter_by(name=data['name']).first()
    assert len(db_obj.language_amounts) == 1


@patch('osemu.extensions.db')
def test_emulator_create_console_nested(mock_db, _db, app):
    mock_db = _db
    
    data = [
        {
            'name': 'Emu 1',
            'consoles': [
                {
                    'name': 'Console 1',
                    'company': {'name': 'company 1'}
                },
                {
                    'name': 'Console 2',
                    'company': {'name': 'company 2'}
                }
            ]
        },
        {
            'name': 'Emu 2',
            'consoles': [
                {
                    'name': 'Console 3',
                    'company': {'name': 'company 3'}
                },
                {
                    'name': 'Console 4',
                    'company': {'name': 'company 4'}
                }
            ]
        },
        {
            'name': 'Emu 3',
            'consoles': [
                {
                    'name': 'Console 5',
                    'company': {'name': 'company 5'}
                }
            ]
        }
    ]

    parsed_data = EmulatorSchema(many=True).load(data)

    get_or_create_obj(EmulatorSchema, parsed_data, True)
    _db.session.commit()

    q = _db.session.query(models.Emulator).all()
    assert len(q) == len(parsed_data)

    q = _db.session.query(models.Console).all()
    assert len(q) == 5

    for d in parsed_data:
        q = _db.session.query(models.Emulator).filter_by(name=d['name']).all()
        assert len(q) == 1

    q = _db.session.query(models.Company).all()
    print([qq.name for qq in q])

    assert len(q) == 5

