from flask_admin.contrib.sqla import ModelView
from osemu.extensions import db, admin
from osemu.api import models

class RefView(ModelView):
    column_hide_backrefs = False

class CompanyView(ModelView):
    column_hide_backrefs = False
    form_columns = ['name', 'consoles']

class ConsoleView(ModelView):
    column_hide_backrefs = False
    form_columns = ['name', 'company', 'release_date', 'end_date', 'short_description', 'wiki_url', 'image_url']
    column_list = ['name', 'company', 'release_date', 'end_date', 'short_description', 'wiki_url', 'image_url']

class LanguageView(ModelView):
    column_hide_backrefs = False
    form_columns = ['name', 'emulators']

class EmulatorView(ModelView):
    column_hide_backrefs = False
    form_columns = ['name', 'git_url', 'gh_stars', 'website_url', 'image_url', 'consoles', 'license', 'short_description', 'latest_update', 'release_date', 'language_amounts']
    column_list = ['name', 'git_url', 'gh_stars', 'website_url', 'image_url', 'consoles', 'license', 'short_description', 'latest_update', 'release_date', 'language_amounts']


def register_admin_views():
    admin.add_view(RefView(models.User, db.session))
    admin.add_view(CompanyView(models.Company, db.session))
    admin.add_view(ConsoleView(models.Console, db.session))
    admin.add_view(RefView(models.EmulatorLanguage, db.session))
    admin.add_view(EmulatorView(models.Emulator, db.session))
    admin.add_view(LanguageView(models.Language, db.session))
    admin.add_view(RefView(models.License, db.session))
