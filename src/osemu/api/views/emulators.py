from flask import Blueprint

from osemu.api.models import Emulator
from osemu.api.schema import EmulatorSchema

from osemu.api.views.util import register_views

emulators_bp = Blueprint('emulators', __name__, url_prefix='/emulators')
emulator_group_view, emulator_entry_view = register_views(emulators_bp, EmulatorSchema, Emulator)
