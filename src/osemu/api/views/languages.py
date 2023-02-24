from flask import Blueprint

from osemu.api.models import Language
from osemu.api.schema import LanguageSchema

from osemu.api.views.base_views import EntryAPI, GroupAPI

languages_bp = Blueprint('languages', __name__, url_prefix='/languages')

languages_bp.add_url_rule('/', view_func=GroupAPI.as_view('language-group', Language, LanguageSchema))
languages_bp.add_url_rule('/<id>/', view_func=EntryAPI.as_view('language-entry', Language, LanguageSchema))
