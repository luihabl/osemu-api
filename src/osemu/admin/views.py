from flask_admin.contrib.sqla import ModelView
from osemu.extensions import db, admin
from osemu.api import models
import flask_login as login

class AdminModelView(ModelView):
    column_hide_backrefs = False

    def is_accessible(self):
        return login.current_user.is_authenticated

class CompanyView(AdminModelView):
    form_columns = ['name', 'consoles']

class ConsoleView(AdminModelView):
    form_columns = ['name', 'company', 'release_date', 'end_date', 'short_description', 'wiki_url', 'image_url']
    column_list = ['name', 'company', 'release_date', 'end_date', 'short_description', 'wiki_url', 'image_url']

class LanguageView(AdminModelView):
    form_columns = ['name', 'emulators']

class EmulatorView(AdminModelView):
    form_columns = ['name', 'git_url', 'gh_stars', 'website_url', 'image_url', 'consoles', 'license', 'short_description', 'latest_update', 'release_date', 'language_amounts']
    column_list = ['name', 'git_url', 'gh_stars', 'website_url', 'image_url', 'consoles', 'license', 'short_description', 'latest_update', 'release_date', 'language_amounts']


def register_admin_views():
    admin.add_view(AdminModelView(models.User, db.session))
    admin.add_view(CompanyView(models.Company, db.session))
    admin.add_view(ConsoleView(models.Console, db.session))
    admin.add_view(AdminModelView(models.EmulatorLanguage, db.session))
    admin.add_view(EmulatorView(models.Emulator, db.session))
    admin.add_view(LanguageView(models.Language, db.session))
    admin.add_view(AdminModelView(models.License, db.session))
