from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from osemu.api.views.consoles import consoles_bp
api_bp.register_blueprint(consoles_bp)

from osemu.api.views.emulators import emulators_bp
api_bp.register_blueprint(emulators_bp)

from osemu.api.views.companies import companies_bp
api_bp.register_blueprint(companies_bp)

from osemu.api.views.languages import languages_bp
api_bp.register_blueprint(languages_bp)

from osemu.api.views.licenses import licenses_bp
api_bp.register_blueprint(licenses_bp)