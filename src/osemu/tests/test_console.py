from osemu.api.models import Console
from osemu.extensions import db

def test_config(app):
    # console = Console(
    #     name='New Console 1',
    #     manufacturer='Manu 1'
    # )
    
    # db.session.add(console)
    # db.session.commit()

    # q = db.session.query(Console).filter_by(name='New Console 1', manufacturer='Manu 1')
    assert 1 == 1

