import json
from abc import ABC, abstractmethod
from osemu.api.views.base_views import get_or_create_obj
import pytest


def post_dict(client, route, d):
    """POST a dictionary to a given route as a JSON.

    Args:
        client (Client): Flask test client
        route (str): API rounte
        d (dict): data to be posted

    Returns:
        response: response with status code after posting.
    """    
    return client.post(route, 
                      data=json.dumps(d),
                      content_type='application/json')

def check_dict(old: dict, new: dict) -> bool:
    """Checks if two dictionaries are equal. Only the keys considered for comparison are
    the ones from `old`.

    Args:
        old (dict): First dictionary to be compared (determines the keys for comparison).
        new (dict): Second dictionary to be compared.

    Returns:
        bool: whether all the keys compared have the same value.
    """    
    
    # This method is done because the lists 
    # can be out of order. But this is O(n^2).
    # So it needs to be optimized. 
    if isinstance(old, list):  
        count = 0
        for o in old:
            for n in new:
                r = check_dict(o, n)
                if r:
                    count += 1
        return count == len(old)

    elif isinstance(old, dict):
        res = [check_dict(v, new[k]) for k,v in old.items()]
        return all(res)
    else:
        return old == new


class _TestAPIBase(ABC):
    ENDPOINT = None
    MODEL = None
    SCHEMA = None


    @abstractmethod
    def create_entries(self, n):
        """Creates `n` entries. If `n==1` then return a dict, else return a list of dicts.
        Must be implemented on child classes of _TestAPIBase.

        Args:
            n (int): number of entries
        """        
        raise NotImplementedError 


class _TestPublicAPIBase(_TestAPIBase):

    def test_unauthorized(self, _db, client):
        data = self.create_entries(1)

        res = client.get(self.ENDPOINT)
        assert res.status_code == 200
        
        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 401

        res = client.put(f'{self.ENDPOINT}{1}/', 
                         data=json.dumps(data), 
                         content_type='application/json')
        assert res.status_code == 401

        res = client.patch(f'{self.ENDPOINT}{1}/', 
                        data=json.dumps(data), 
                        content_type='application/json')
        assert res.status_code == 401

        res = client.delete(f'{self.ENDPOINT}{1}/')
        assert res.status_code == 401


    def test_get(self, client, _db):
        data = self.create_entries(3)

        objs = get_or_create_obj(self.SCHEMA, data)
        _db.session.add_all(objs)
        _db.session.commit()

        res = client.get(self.ENDPOINT)
        assert res.status_code == 200

        res_data = json.loads(res.data)
        assert check_dict(data, res_data)


@pytest.mark.usefixtures('authenticated_user')
class _TestPrivateAPIBase(_TestAPIBase):

    def test_post(self, _db, client):

        data = self.create_entries(1)
        res = post_dict(client, self.ENDPOINT, data)

        assert res.status_code == 200

        q = _db.session.query(self.MODEL).all()
        assert len(q) == 1

        assert check_dict(data, self.SCHEMA().dump(q[0]))


    def test_post_many(self, _db, client):
        data = self.create_entries(3)

        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 200

        q = _db.session.query(self.MODEL).all()
        assert len(q) == len(data)

        assert check_dict(data, self.SCHEMA(many=True).dump(q))


    def test_post_fail_duplicate(self, client, _db):
        data = [self.create_entries(1), self.create_entries(1)]

        res = post_dict(client, self.ENDPOINT, data)

        assert res.status_code == 400

        res = client.get(self.ENDPOINT)
        res_data = json.loads(res.data)

        assert len(res_data) == 0

    def test_patch(self, client, _db):
        data = self.create_entries(1)

        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 200

        # Hard-coded 'name' key because all models have name property
        # Can change to a string read from the schema class
        res = client.get(self.ENDPOINT, query_string={'name': data['name']})
        assert res.status_code == 200

        id = json.loads(res.data)['id']
        new_data = {
            'name' : 'New name'
        }
        
        res = client.patch(f'{self.ENDPOINT}{id}/', 
                        data=json.dumps(new_data), 
                        content_type='application/json')

        assert res.status_code == 200

        res = client.get(f'{self.ENDPOINT}{id}/')
        assert res.status_code == 200

        res_data = json.loads(res.data)
        assert res_data['name'] == new_data['name']


    def test_put(self, client, _db):

        data = self.create_entries(2)

        res = post_dict(client, self.ENDPOINT, data[0])
        assert res.status_code == 200

        res = client.get(self.ENDPOINT, query_string={'name': data[0]['name']})
        assert res.status_code == 200

        id = json.loads(res.data)['id']
        
        res = client.put(f'{self.ENDPOINT}{id}/', 
                        data=json.dumps(data[1]), 
                        content_type='application/json')

        assert res.status_code == 200

        res = client.get(f'{self.ENDPOINT}{id}/')
        assert res.status_code == 200

        res_data = json.loads(res.data)
        assert check_dict(data[1], res_data)

    def test_delete(self, client, _db):
        data = self.create_entries(3)

        res = post_dict(client, self.ENDPOINT, data)
        assert res.status_code == 200

        q = _db.session.query(self.MODEL).all()
        assert len(q) == len(data)

        id_0 = q[0].id
        client.delete(f'{self.ENDPOINT}{id_0}/')

        q = _db.session.query(self.MODEL).all()
        assert len(q) == len(data) - 1

        q_data = self.SCHEMA(many=True).dump(q)

        assert check_dict(data[1:], q_data)







