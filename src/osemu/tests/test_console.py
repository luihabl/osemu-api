"""
Test consoles API
"""

from osemu.api.models import Console, Company
from osemu.api.schema import ConsoleSchema
from .conftest import _TestAPIBase


class TestConsoleAPI(_TestAPIBase):
    ENDPOINT = '/api/consoles/'
    MODEL = Console
    SCHEMA = ConsoleSchema

    def create_entries(self, n):
        
        def entry(i):
            return {
                'name': f'Console {i}',
                'company': {'name': f'company {i}'}
            }

        if n == 1:
            return entry(1)
        else:
            return [entry(i) for i in range(n)]

    def test_post(self, _db, client):
        super().test_post(_db, client)

        q = _db.session.query(Company).all()
        assert len(q) == 1

