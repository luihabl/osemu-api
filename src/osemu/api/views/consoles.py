from flask import Blueprint, jsonify

from osemu.api.models import Console
from osemu.api.schema import ConsoleSchema, EmulatorSchema
from osemu.extensions import db

from osemu.api.views.util import register_views

consoles_bp = Blueprint('consoles', __name__, url_prefix='/consoles')



@consoles_bp.route('/<id>/emulators/', methods=['GET'])
def emulators_for_console_view(id):
    """ Get emulators for a given console id.
    ---
    get:
      description: Get `Emulator`s for a given `Console` id.
      tags:
        - Console
      parameters:
        - in: path
          name: id
          schema:
            type: string
            format: uuid
      responses:
        200:
          description: Get all `$name` objects.
          content:
            application/json:
              schema:
                type: array
                items: EmulatorSchema
        404:
          description: ID not found.
    """

    console = db.session.get(Console, id)

    if not console:
        return jsonify(message='ID not found.'), 404

    return EmulatorSchema(many=True).dump(console.emulators)


console_group_view, console_entry_view = register_views(consoles_bp, ConsoleSchema, Console)
