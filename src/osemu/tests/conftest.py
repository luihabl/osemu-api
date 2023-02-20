import pytest
from osemu import create_app
from osemu import config

@pytest.fixture
def app():
    app = create_app(config.TestingConfig)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
    