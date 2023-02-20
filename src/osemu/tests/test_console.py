from .conftest import *

def test_config(app):
    assert app.config['TESTING']

