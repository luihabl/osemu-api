from osemu.api.models import Console
from osemu.extensions import db

def test_config(_db, app):

    console = Console(
        name='New Console 1',
        manufacturer='Manu 1'
    )
    
    _db.session.add(console)
    _db.session.commit()

    q = db.session.query(Console).filter_by(name='New Console 1', manufacturer='Manu 1')
    
    assert q.count() == 1

def test_config2(_db, app):

    console = Console(
        name='New Console 1',
        manufacturer='Manu 1'
    )
    
    _db.session.add(console)
    _db.session.commit()

    q = _db.session.query(Console).filter_by(name='New Console 1', manufacturer='Manu 1')
    
    assert q.count() == 1

