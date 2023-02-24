"""
Test consoles API
"""

from osemu.api.models import Console, Company
from osemu.extensions import db
import json

def _post_dict(client, route, d):
    return client.post(route, 
                      data=json.dumps(d),
                      content_type='application/json')


def test_post_console(client, _db):

    data = {
        'name': 'Console 1',
        'company': {'name': 'company 1'}
    }

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 200

    q = _db.session.query(Console).all()
    assert len(q) == 1

    assert data['name'] == q[0].name
    assert data['company']['name'] == q[0].company.name

    q = _db.session.query(Company).all()
    assert len(q) == 1


def test_post_many_consoles(client, _db):
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

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 200

    q = _db.session.query(Console).all()
    assert len(q) == len(data)

    for d in data:
        q = _db.session.query(Console).filter_by(name=d['name']).first()
        assert d['name'] == q.name
        assert d['company']['name'] == q.company.name


def test_post_console_fail_duplicate(client, _db):
    data = [
        {
            'name': 'Console 1',
            'company': {'name': 'company 1'}
        },
        {
            'name': 'Console 1',
            'company': {'name': 'company 1'}
        }
    ]

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 400

    res = client.get('/api/consoles/')
    res_data = json.loads(res.data)

    assert len(res_data) == 0



def test_get_consoles(client, _db):
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

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 200

    res = client.get('/api/consoles/')
    res_data = json.loads(res.data)

    for rd, d in zip(res_data, data):
        assert rd['name'] == d['name']
        assert rd['company']['name'] == d['company']['name']



def test_patch_consoles(client, _db):
    data = {
                'name': 'Console 2',
                'company': {'name': 'company 1'}
           }

    res = _post_dict(client, '/api/consoles/', data)
    assert res.status_code == 200

    res = client.get('/api/consoles/', query_string={'name': data['name']})
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = {
        'name' : 'New console'
    }
    
    res = client.patch(f'/api/consoles/{id}/', 
                       data=json.dumps(new_data), 
                       content_type='application/json')

    assert res.status_code == 200

    res = client.get(f'/api/consoles/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert res_data['name'] == new_data['name']


def test_put_consoles(client, _db):
    data = {
                'name': 'Console 2',
                'company': {'name': 'company 1'}
           }

    res = _post_dict(client, '/api/consoles/', data)
    assert res.status_code == 200

    res = client.get('/api/consoles/', query_string={'name': data['name']})
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = {
        'name' : 'New console',
        'company' : {'name': 'Nontendo'}
    }
    
    res = client.put(f'/api/consoles/{id}/', 
                     data=json.dumps(new_data), 
                     content_type='application/json')

    assert res.status_code == 200

    res = client.get(f'/api/consoles/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert res_data['name'] == new_data['name']
    assert res_data['company']['name'] == new_data['company']['name']



