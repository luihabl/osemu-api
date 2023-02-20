import pytest
from osemu import create_app
from osemu import config
from osemu.extensions import db
import os

@pytest.fixture(scope='session')
def app(request):
    app = create_app(config=config.TestingConfig)

    # with app.app_context():
    #     db.create_all()
    #     yield app
    #     db.session.remove()
    #     db.drop_all()
    
    return app
    