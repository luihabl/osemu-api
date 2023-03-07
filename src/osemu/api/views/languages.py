from flask import Blueprint

from osemu.api.models import Language
from osemu.api.schema import LanguageSchema

from osemu.api.views.util import register_views

languages_bp = Blueprint('languages', __name__, url_prefix='/languages')
language_group_view, language_entry_view = register_views(languages_bp, LanguageSchema, Language)

