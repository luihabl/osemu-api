"""
Test languages API
"""

from osemu.api.models import Language
from osemu.api.schema import LanguageSchema
from osemu.tests.conftest import _TestAPIBase

class TestCompaniesAPI(_TestAPIBase):
    ENDPOINT = '/api/languages/'
    MODEL = Language
    SCHEMA = LanguageSchema

    def create_entries(self, n):
        d = [{'name': f'lang {i}'} for i in range(n)]
        if len(d) == 1:
            return d[0]
        return d
        
    
