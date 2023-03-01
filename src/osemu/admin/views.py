from flask_admin.contrib.sqla import ModelView
from osemu.extensions import db, admin
from osemu.api import models
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    email = fields.EmailField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_login(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid information')

        # we're comparing the plaintext pw with the the hash from the db
        if not check_password_hash(user.password, self.password.data):
        # to compare plain text passwords use
        # if user.password != self.password.data:
            raise validators.ValidationError('Invalid information')

    def get_user(self):
        return db.session.query(models.User).filter_by(email=self.email.data).first()





class RefView(ModelView):
    column_hide_backrefs = False

class CompanyView(RefView):
    form_columns = ['name', 'consoles']

class ConsoleView(RefView):
    form_columns = ['name', 'company', 'release_date', 'end_date', 'short_description', 'wiki_url', 'image_url']
    column_list = ['name', 'company', 'release_date', 'end_date', 'short_description', 'wiki_url', 'image_url']

class LanguageView(RefView):
    form_columns = ['name', 'emulators']

class EmulatorView(RefView):
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
