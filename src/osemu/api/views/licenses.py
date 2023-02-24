from flask import Blueprint

from osemu.api.models import License
from osemu.api.schema import LicenseSchema

from osemu.api.views.base_views import EntryAPI, GroupAPI

licenses_bp = Blueprint('licenses', __name__, url_prefix='/licenses')

licenses_bp.add_url_rule('/', view_func=GroupAPI.as_view('license-group', License, LicenseSchema))
licenses_bp.add_url_rule('/<id>/', view_func=EntryAPI.as_view('license-entry', License, LicenseSchema))
