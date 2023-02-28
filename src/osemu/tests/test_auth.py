"""
Test authentication
"""

import pytest
from osemu.api import models
from .base_api_tests import post_dict
from osemu.api import models
from werkzeug.security import check_password_hash
from flask_login import current_user

def test_user_create(app, client, _db):
    data = {
        'email': 'example@example.com',
        'password': 'test123'
    }
    
    res = post_dict(client, '/api/auth/signup', data)
    assert res.status_code == 200

    q = _db.session.query(models.User).all()
    assert len(q) == 1
    assert q[0].email == data['email']
    assert check_password_hash(q[0].password, data['password'])

def test_user_error_duplicate_email(app, client, _db):
    data1 = {
        'email': 'example@example.com',
        'password': 'test123'
    }
    
    res = post_dict(client, '/api/auth/signup', data1)
    print(res.data)
    assert res.status_code == 200

    data2 = {
        'email': 'example@example.com',
        'password': 'testest111'
    }
    
    res = post_dict(client, '/api/auth/signup', data2)
    print(res.data)
    assert res.status_code == 400

    q = _db.session.query(models.User).all()
    assert len(q) == 1
    assert q[0].email == data1['email']
    assert check_password_hash(q[0].password, data1['password'])

def test_login(app, client, _db):

    data = {
        'email': 'example@example.com',
        'password': 'test123'
    }

    res = post_dict(client, '/api/auth/login', data)
    assert res.status_code == 400
    
    res = post_dict(client, '/api/auth/signup', data)
    assert res.status_code == 200

    res = post_dict(client, '/api/auth/logout', data)
    assert res.status_code == 401

    res = post_dict(client, '/api/auth/login', data)
    assert res.status_code == 200

    res = post_dict(client, '/api/auth/logout', data)
    assert res.status_code == 200

    data['password'] = 'ttest123'
    res = post_dict(client, '/api/auth/login', data)
    assert res.status_code == 400

    data['password'] = 'test123'
    res = post_dict(client, '/api/auth/login', data)
    assert res.status_code == 200

    res = client.get('/api/auth/user')
    assert res.status_code == 200
    
    res = post_dict(client, '/api/auth/logout', data)
    assert res.status_code == 200

    res = client.get('/api/auth/user')
    assert res.status_code == 401


