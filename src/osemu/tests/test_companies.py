"""
Test companies API
"""

from osemu.api.models import Company
from osemu.api.schema import CompanySchema
from osemu.tests.base_api_tests import _TestAPIBase, _post_dict

class TestCompaniesAPI(_TestAPIBase):
    ENDPOINT = '/api/companies/'
    MODEL = Company
    SCHEMA = CompanySchema

    def create_entries(self, n):
        d = [{'name': f'company {i}'} for i in range(n)]
        if len(d) == 1:
            return d[0]
        return d
        
    
