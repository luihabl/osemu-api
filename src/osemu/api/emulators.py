from flask import Blueprint

from .models import Emulator
from .schema import EmulatorSchema

from .base_views import EntryAPI, GroupAPI

emulators_bp = Blueprint('emulators', __name__, url_prefix='/emulators')

emulators_bp.add_url_rule('/', view_func=GroupAPI.as_view('console-group', Emulator, EmulatorSchema))
emulators_bp.add_url_rule('/<id>', view_func=EntryAPI.as_view('console-entry', Emulator, EmulatorSchema))
