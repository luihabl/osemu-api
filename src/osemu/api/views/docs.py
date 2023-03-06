"""Route for OpenAPI spec."""

from osemu.docs.specs import spec
from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint

docs_bp = Blueprint('docs', __name__, url_prefix='/docs')

@docs_bp.route('/spec', methods=['GET'])
def spec_json():
    return spec.to_dict()

swaggerui_bp = get_swaggerui_blueprint(
    base_url='/api/docs', 
    api_url='/api/docs/spec'
)
