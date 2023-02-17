from flask import Blueprint

from .models import Console
from .schema import ConsoleSchema

from .base_views import EntryAPI, GroupAPI

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')

consoles_bp.add_url_rule('/', view_func=GroupAPI.as_view('console-group', Console, ConsoleSchema))
consoles_bp.add_url_rule('/<id>', view_func=EntryAPI.as_view('console-entry', Console, ConsoleSchema))
