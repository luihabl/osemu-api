"""
Test emulators API
"""

from osemu.api.models import Emulator
import json


def _post_dict(client, route, d):
    return client.post(route, 
                      data=json.dumps(d),
                      content_type='application/json')


def test_post_emulator(client, _db):

    data1 = {
        'name': 'Emu 1'
    }

    res = _post_dict(client, '/api/emulators/', data1)
    assert res.status_code == 200

    q = _db.session.query(Emulator).all()
    assert len(q) == 1


    data2 = [
        {'name': 'Emu 2'},
        {'name': 'Emu 3'}
    ]

    res = _post_dict(client, '/api/emulators/', data2)
    assert res.status_code == 200

    q = _db.session.query(Emulator).all()
    assert len(q) == 3

    assert data1['name'] == q[0].name
    assert data2[0]['name'] == q[1].name
    assert data2[1]['name'] == q[2].name


def test_post_emulator_fail_duplicate(client, _db):
    data = [
        {'name': 'Emu 2'},
        {'name': 'Emu 2'}
    ]

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 400


def test_get_emulators(client, _db):
    data = [
        {'name': 'Emu 1'},
        {'name': 'Emu 2'}
    ]

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 200

    res = client.get('/api/emulators/')
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert len(res_data) == len(data)

    # this keeps only the 'name' key
    res_data = [{k:v for k, v in d.items() if (k == 'name')} for d in res_data]

    assert res_data == data


def test_patch_emulators(client, _db):
    data = {
                'name': 'Emulator 1'
           }

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 200

    res = client.get('/api/emulators/', query_string=data)
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = {
        'name' : 'New emulator'
    }
    
    res = client.patch(f'/api/emulators/{id}/', 
                       data=json.dumps(new_data), 
                       content_type='application/json')

    assert res.status_code == 200

    res = client.get(f'/api/emulators/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert res_data['name'] == new_data['name']


def test_put_emulators(client, _db):
    data = { 'name': 'Emulator 2' }

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 200

    res = client.get('/api/emulators/', query_string=data)
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = { 'name' : 'New console' }
    
    res = client.put(f'/api/emulators/{id}/', 
                     data=json.dumps(new_data), 
                     content_type='application/json')

    assert res.status_code == 200

    res = client.get(f'/api/emulators/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)
    assert res_data['name'] == new_data['name']


def test_post_emulator_nested_console(client, _db):

    data = [
        {
            'name': 'Emu 1',
            'consoles': [
                {
                    'name': 'Console 1',
                    'company': 'company 1'
                },
                {
                    'name': 'Console 2',
                    'company': 'company 1'
                }
            ]
        },
        {
            'name': 'Emu 2',
            'consoles': [
                {
                    'name': 'Console 3',
                    'company': 'company 1'
                },
                {
                    'name': 'Console 4',
                    'company': 'company 1'
                }
            ]
        },
        {
            'name': 'Emu 3',
            'consoles': [
                {
                    'name': 'Console 5',
                    'company': 'company 1'
                }
            ]
        }
    ]

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 200

    res = client.get('/api/emulators/')
    res_data = json.loads(res.data)
    assert len(res_data) == 3

    res = client.get('/api/consoles/')
    res_data = json.loads(res.data)
    assert len(res_data) == 5

    data2 =  {
        'name': 'Emu 4',
        'consoles': [
            {
                'name': 'Console 1',
                'company': 'company 1'
            },
            {
                'name': 'Console 2',
                'company': 'company 1'
            }
        ]
    }

    res = _post_dict(client, '/api/emulators/', data2)
    assert res.status_code == 200

    res = client.get('/api/emulators/')
    res_data = json.loads(res.data)
    assert len(res_data) == 4

    res = client.get('/api/consoles/')
    res_data = json.loads(res.data)
    assert len(res_data) == 5
    
    i = 0
    for e in data:
        for c in e['consoles']:
            assert c['name'] == res_data[i]['name']
            i += 1
            

def test_patch_emulator_nested_console(client, _db):
    data = [
        {
            'name': 'Emu 1',
            'consoles': [
                {
                    'name': 'Console 1',
                    'company': 'company 1'
                },
                {
                    'name': 'Console 2',
                    'company': 'company 1'
                }
            ]
        },
        {
            'name': 'Emu 2',
            'consoles': [
                {
                    'name': 'Console 3',
                    'company': 'company 1'
                },
                {
                    'name': 'Console 4',
                    'company': 'company 1'
                }
            ]
        }
    ]

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 200

    res = client.get('/api/emulators/', query_string={'name': data[0]['name']})
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = {
        'consoles' : [
             {
                'name': 'Console 2',
                'company': 'company 1'
            },
            {
                'name': 'Console 5',
                'company': 'company 1'
            }
        ]
    }
    
    res = client.patch(f'/api/emulators/{id}/', 
                       data=json.dumps(new_data), 
                       content_type='application/json')
    

    assert res.status_code == 200

    res = client.get(f'/api/emulators/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)

    for c, r in zip(new_data['consoles'], res_data['consoles']):
        for k, v in c.items():
            assert v == r[k]

    res = client.get(f'/api/consoles/')
    assert res.status_code == 200
    res_data = json.loads(res.data)
    assert len(res_data) == 5


def test_put_emulator_nested_console(client, _db):
    data = [
        {
            'name': 'Emu 1',
            'consoles': [
                {
                    'name': 'Console 1',
                    'company': 'company 1'
                },
                {
                    'name': 'Console 2',
                    'company': 'company 1'
                }
            ]
        },
        {
            'name': 'Emu 2',
            'consoles': [
                {
                    'name': 'Console 3',
                    'company': 'company 1'
                },
                {
                    'name': 'Console 4',
                    'company': 'company 1'
                }
            ]
        }
    ]

    res = _post_dict(client, '/api/emulators/', data)
    assert res.status_code == 200

    res = client.get('/api/emulators/', query_string={'name': data[0]['name']})
    assert res.status_code == 200

    id = json.loads(res.data)['id']
    new_data = {
        'name': 'Emu 3',
        'consoles': [
            {
                'name': 'Console 2',
                'company': 'company 1'
            },
            {
                'name': 'Console 4',
                'company': 'company 1'
            }
        ]
    }
    
    res = client.put(f'/api/emulators/{id}/', 
                       data=json.dumps(new_data), 
                       content_type='application/json')
    

    assert res.status_code == 200

    res = client.get(f'/api/emulators/{id}/')
    assert res.status_code == 200

    res_data = json.loads(res.data)

    assert new_data['name'] == res_data['name']
    for c, r in zip(new_data['consoles'], res_data['consoles']):
        for k, v in c.items():
            assert v == r[k]


    
