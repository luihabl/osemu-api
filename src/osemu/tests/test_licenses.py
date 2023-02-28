"""
Test licenses API
"""

from osemu.api.models import License
from osemu.api.schema import LicenseSchema
from osemu.tests.base_api_tests import _TestPublicAPIBase, _TestPrivateAPIBase

def _create_entries(n):
        d = [{'name': f'license {i}', 'url': 'www.exemple{i}.com'} for i in range(n)]
        if len(d) == 1:
            return d[0]
        return d

class TestLicensesAPI(_TestPublicAPIBase):
    ENDPOINT = '/api/licenses/'
    MODEL = License
    SCHEMA = LicenseSchema

    def create_entries(self, n):
        return _create_entries(n)

class TestLicensesAPI(_TestPrivateAPIBase):
    ENDPOINT = '/api/licenses/'
    MODEL = License
    SCHEMA = LicenseSchema

    def create_entries(self, n):
        return _create_entries(n)

        
    
