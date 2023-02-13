from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

from .consoles import consoles_bp
api_bp.register_blueprint(consoles_bp)

from .emulators import emulators_bp
api_bp.register_blueprint(emulators_bp)