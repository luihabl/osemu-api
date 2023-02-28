"""
Test languages API
"""

from osemu.api.models import Language
from osemu.api.schema import LanguageSchema
from osemu.tests.base_api_tests import _TestPublicAPIBase, _TestPrivateAPIBase

def _create_entries(n):
        d = [{'name': f'lang {i}'} for i in range(n)]
        if len(d) == 1:
            return d[0]
        return d
        
class TestLanguagesAPI(_TestPublicAPIBase):
    ENDPOINT = '/api/languages/'
    MODEL = Language
    SCHEMA = LanguageSchema

    def create_entries(self, n):
        return _create_entries(n)
        

class TestLanguagesAPI(_TestPrivateAPIBase):
    ENDPOINT = '/api/languages/'
    MODEL = Language
    SCHEMA = LanguageSchema

    def create_entries(self, n):
        return _create_entries(n)
    
