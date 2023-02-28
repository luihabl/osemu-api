"""
Test companies API
"""

from osemu.api.models import Company
from osemu.api.schema import CompanySchema
from osemu.tests.base_api_tests import _TestPrivateAPIBase, _TestPublicAPIBase

def _create_entries(n):
        d = [{'name': f'company {i}'} for i in range(n)]
        if len(d) == 1:
            return d[0]
        return d

class TestCompaniesPrivateAPI(_TestPrivateAPIBase):
    ENDPOINT = '/api/companies/'
    MODEL = Company
    SCHEMA = CompanySchema

    def create_entries(self, n):
        return _create_entries(n)
        
    
class TestCompaniesPublicAPI(_TestPublicAPIBase):
    ENDPOINT = '/api/companies/'
    MODEL = Company
    SCHEMA = CompanySchema

    def create_entries(self, n):
        return _create_entries(n)
        
    
