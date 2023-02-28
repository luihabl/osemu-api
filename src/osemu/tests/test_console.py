"""
Test consoles API
"""

from osemu.api.models import Console, Company
from osemu.api.schema import ConsoleSchema
from osemu.tests.base_api_tests import _TestPrivateAPIBase, _TestPublicAPIBase

def _create_entries(n):
        
        def entry(i):
            return {
                'name': f'Console {i}',
                'company': {'name': f'company {i}'}
            }

        if n == 1:
            return entry(1)
        else:
            return [entry(i) for i in range(n)]


class TestConsolePublicAPI(_TestPublicAPIBase):
    ENDPOINT = '/api/consoles/'
    MODEL = Console
    SCHEMA = ConsoleSchema

    def create_entries(self, n):
        return _create_entries(n)


class TestConsolePrivateAPI(_TestPrivateAPIBase):
    ENDPOINT = '/api/consoles/'
    MODEL = Console
    SCHEMA = ConsoleSchema

    def create_entries(self, n):
        return _create_entries(n)

    def test_post(self, _db, client):
        super().test_post(_db, client)

        q = _db.session.query(Company).all()
        assert len(q) == 1

