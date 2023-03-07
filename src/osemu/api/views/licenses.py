from flask import Blueprint

from osemu.api.models import License
from osemu.api.schema import LicenseSchema

from osemu.api.views.util import register_views

licenses_bp = Blueprint('licenses', __name__, url_prefix='/licenses')
license_group_view, license_entry_view = register_views(licenses_bp, LicenseSchema, License)

