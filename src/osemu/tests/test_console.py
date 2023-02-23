"""
Test consoles API
"""

from osemu.api.models import Console
from osemu.extensions import db
import json

def _post_dict(client, route, d):
    return client.post(route, 
                      data=json.dumps(d),
                      content_type='application/json')


def test_post_console(client, _db):

    data = {
        'name': 'Console 1',
        'company': 'company 1'
    }

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 200

    q = _db.session.query(Console).all()
    assert len(q) == 1

    for k,v in data.items():
        assert v == q[0].__dict__[k]


def test_post_many_consoles(client, _db):
    data = [
        {
            'name': 'Console 1',
            'company': 'company 1'
        },
        {
            'name': 'Console 2',
            'company': 'company 1'
        },
        {
            'name': 'Console 3',
            'company': 'company 1'
        }
    ]

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 200

    q = _db.session.query(Console).all()
    assert len(q) == len(data)

    for d in data:
        q = _db.session.query(Console).filter_by(**d).first()
        assert d['name'] == q.name
        assert d['company'] == q.company


def test_post_console_fail_duplicate(client, _db):
    data = [
        {
            'name': 'Console 1',
            'company': 'company 1'
        },
        {
            'name': 'Console 1',
            'company': 'company 1'
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
            'company': 'company 1'
        },
        {
            'name': 'Console 2',
            'company': 'company 1'
        },
        {
            'name': 'Console 3',
            'company': 'company 1'
        }
    ]

    res = _post_dict(client, '/api/consoles/', data)

    assert res.status_code == 200

    res = client.get('/api/consoles/')
    res_data = json.loads(res.data)
    
    # this just removes the 'id' key
    res_data = [{k:v for k, v in d.items() if k != 'id'} for d in res_data]

    assert data == res_data


def test_patch_consoles(client, _db):
    data = {
                'name': 'Console 2',
                'company': 'company 1'
           }

    res = _post_dict(client, '/api/consoles/', data)
    assert res.status_code == 200

    res = client.get('/api/consoles/', query_string=data)
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
                'company': 'company 1'
           }

    res = _post_dict(client, '/api/consoles/', data)
    assert res.status_code == 200

    res = client.get('/api/consoles/', query_string=data)
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = {
        'name' : 'New console',
        'company' : 'Nontendo'
    }
    
    res = client.put(f'/api/consoles/{id}/', 
                     data=json.dumps(new_data), 
                     content_type='application/json')

    assert res.status_code == 200

    res = client.get(f'/api/consoles/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert res_data['name'] == new_data['name']
    assert res_data['company'] == new_data['company']



