"""Route for OpenAPI spec."""

from osemu.docs.specs import spec
from flask import Blueprint

spec_bp = Blueprint('spec', __name__, url_prefix='/spec')

@spec_bp.route('/', methods=['GET'])
def spec_json():
    return spec.to_dict()