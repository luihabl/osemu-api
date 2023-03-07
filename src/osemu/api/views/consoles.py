from flask import Blueprint

from osemu.api.models import Console
from osemu.api.schema import ConsoleSchema

from osemu.api.views.util import register_views

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')
console_group_view, console_entry_view = register_views(consoles_bp, ConsoleSchema, Console)
