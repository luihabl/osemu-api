from flask import Blueprint

from osemu.api.models import Company
from osemu.api.schema import CompanySchema

from osemu.api.views.util import register_views

companies_bp = Blueprint('companies', __name__, url_prefix='/companies')
company_group_view, company_entry_view = register_views(companies_bp, CompanySchema, Company)