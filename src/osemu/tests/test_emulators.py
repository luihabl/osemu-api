"""
Test emulators API
"""

from osemu.api.models import Emulator, EmulatorLanguage, Language
from osemu.api.schema import EmulatorSchema
from osemu.tests.base_api_tests import _TestPrivateAPIBase, _TestPublicAPIBase, post_dict, check_dict
import json

def _create_entries(n):
        def entry(i):
            return {
                'name': f'Emu {i}',
                'consoles': [
                    {
                        'name': f'Console {2*i}',
                        'company': {'name': f'company {2*i}'}
                    }, 
                    {
                        'name': f'Console {2*i+1}',
                        'company': {'name': f'company {2*i+1}'}
                    }
                ]
            }

        if n == 1:
            return entry(1)
        else:
            return [entry(i) for i in range(n)]


class TestEmulatorAPI(_TestPublicAPIBase):
    ENDPOINT = '/api/emulators/'
    MODEL = Emulator
    SCHEMA = EmulatorSchema

    def create_entries(self, n):
        return _create_entries(n)


class TestEmulatorAPI(_TestPrivateAPIBase):
    ENDPOINT = '/api/emulators/'
    MODEL = Emulator
    SCHEMA = EmulatorSchema

    def create_entries(self, n):
        return _create_entries(n)


    def test_emu_license(self, client, _db):
        data = self.create_entries(3)
        data[0]['license'] = {'name': 'license 1', 'url': 'www.example.com'}
        data[2]['license'] = {'name': 'license 2'}
        post_dict(client, self.ENDPOINT, data)

        res = client.get('/api/licenses/')
        assert res.status_code == 200
        
        res_data = json.loads(res.data)
        assert len(res_data) == 2
        assert check_dict(data[0]['license'], res_data[0])
        assert check_dict(data[2]['license'], res_data[1])

        res = client.delete(f'/api/licenses/{res_data[0]["id"]}/')
        assert res.status_code == 200

        res = client.delete(f'/api/licenses/{res_data[1]["id"]}/')
        assert res.status_code == 200

        res = client.get(self.ENDPOINT)
        assert res.status_code == 200
        res_data = json.loads(res.data)

        assert res_data[0]['license'] == None
        assert res_data[1]['license'] == None
        assert res_data[2]['license'] == None


    def test_emu_programming_languages(self, client, _db):
        data = self.create_entries(1)
        data['languages'] = [
            {'language': {'name': 'C++'}, 'amount': 0.2},
            {'language': {'name': 'Python'}, 'amount': 0.8}
        ]

        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 200

        res = client.get('/api/languages/')
        res_data = json.loads(res.data)
        assert len(res_data) == 2


        data2 = self.create_entries(3)[-1]
        data2['languages'] = [
            {'language': {'name': 'C++'}, 'amount': 0.2},
            {'language': {'name': 'Go'}, 'amount': 0.8}
        ]

        res = post_dict(client, self.ENDPOINT, data2)
        assert res.status_code == 200

        res = client.get('/api/languages/')
        assert res.status_code == 200
        res_data = json.loads(res.data)
        print(res_data)
        assert len(res_data) == 3

        q = _db.session.query(Language).all()
        assert len(q) == 3
        q = _db.session.query(EmulatorLanguage).all()
        assert len(q) == 4


    def test_post_emulator_nested_console(self, client, _db):

        data = self.create_entries(3)

        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 200

        res = client.get(self.ENDPOINT)
        res_data = json.loads(res.data)
        assert len(res_data) == 3

        res = client.get('/api/consoles/')
        res_data = json.loads(res.data)
        assert len(res_data) == 6

        data2 = self.create_entries(4)[-1]
        data2['consoles'] =  [
            {
                'name': 'Console 1',
                'company': {'name': 'company 1'}
            },
            {
                'name': 'Console 2',
                'company': {'name': 'company 1'}
            }
        ]

        res = post_dict(client, self.ENDPOINT, data2)
        assert res.status_code == 200

        res = client.get(self.ENDPOINT)
        res_data = json.loads(res.data)
        assert len(res_data) == 4

        res = client.get('/api/consoles/')
        res_data = json.loads(res.data)
        assert len(res_data) == 6
                    

    def test_patch_emulator_nested_console(self, client, _db):
        
        data = self.create_entries(2)

        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 200

        res = client.get(self.ENDPOINT, query_string={'name': data[0]['name']})
        assert res.status_code == 200

        id = json.loads(res.data)['id']
        new_data = {
            'consoles' : [
                {
                    'name': 'Console 2',
                    'company': {'name': 'company 1'}
                },
                {
                    'name': 'Console 5',
                    'company': {'name': 'company 1'}
                }
            ]
        }
        
        res = client.patch(f'{self.ENDPOINT}{id}/', 
                        data=json.dumps(new_data), 
                        content_type='application/json')
        

        assert res.status_code == 200

        res = client.get(f'{self.ENDPOINT}{id}/')
        assert res.status_code == 200

        res_data = json.loads(res.data)

        count = 0
        for c0 in new_data['consoles']:
            for c1 in res_data['consoles']:
                if c0['name'] == c1['name'] and  c0['company']['name'] == c1['company']['name']:
                    count += 1

        # Have to do this count method since the lists were in different order
        assert count == 2

        res = client.get(f'/api/consoles/')
        assert res.status_code == 200
        res_data = json.loads(res.data)
        assert len(res_data) == 5

