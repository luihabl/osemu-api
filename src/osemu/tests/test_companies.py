"""
Test companies API
"""

from .conftest import _post_dict
from osemu.api.models import Company
from osemu.api.schema import CompanySchema
from osemu.tests.conftest import _TestAPIBase

class TestCompaniesAPI(_TestAPIBase):
    ENDPOINT = '/api/companies/'
    MODEL = Company
    SCHEMA = CompanySchema

    def create_entries(self, n):
        d = [{'name': f'company {i}'} for i in range(n)]
        if len(d) == 1:
            return d[0]
        return d
        
    
