import os
import pytest
from osemu import create_app
from osemu import config
from osemu.extensions import db
from osemu.api.models import User
from flask_login import login_user, logout_user

@pytest.fixture(scope='session')
def app():
    
    app = create_app(config=config.TestingConfig, init_db=False)

    with app.app_context():
        yield app

@pytest.fixture()
def client(app):
    return app.test_client()
    
@pytest.fixture(scope='function')
def _db(app):
    if 'USING_TEST_DB' in os.environ:
        db.drop_all()
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()
    else:
        print('Not working with test database, so tests were aborted to avoid data loss.')
        exit(1)


@pytest.fixture(scope='class')
def authenticated_user(app):   

    with app.test_request_context():
        user = User(**{'email': 'test@test.com', 'password': 'test'})

        login_user(user=user)
        yield
        logout_user()
