from flask import Blueprint

from osemu.api.models import Company
from osemu.api.schema import CompanySchema

from osemu.api.views.base_views import EntryAPI, GroupAPI

companies_bp = Blueprint('companies', __name__, url_prefix='/companies')

companies_bp.add_url_rule('/', view_func=GroupAPI.as_view('company-group', Company, CompanySchema))
companies_bp.add_url_rule('/<id>/', view_func=EntryAPI.as_view('company-entry', Company, CompanySchema))
