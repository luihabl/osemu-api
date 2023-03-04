from flask_admin import AdminIndexView, expose, helpers
from wtforms import form, fields, validators
from werkzeug.security import check_password_hash
from osemu.api import models
from flask import redirect, request, url_for
import flask_login as login

class LoginForm(form.Form):
    email = fields.EmailField(validators=[validators.InputRequired()])
    password = fields.PasswordField(validators=[validators.InputRequired()])

    def validate_email(self, field):
        user = self.get_user()

        if user is None:
            raise validators.ValidationError('Invalid information')
        if not check_password_hash(user.password, self.password.data):
            raise validators.ValidationError('Invalid information')

    def get_user(self):
        return models.get_one(models.User, email=self.email.data)


class LoginAdminIndexView(AdminIndexView):
        
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(LoginAdminIndexView, self).index()
    
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        # handle user login
        form = LoginForm(request.form)
        if helpers.validate_form_on_submit(form):
            user = form.get_user()
            login.login_user(user)

        if login.current_user.is_authenticated:
            return redirect(url_for('.index'))

        self._template_args['form'] = form
        return super(LoginAdminIndexView, self).index()
    
    @expose('/logout/')
    def logout_view(self):
        login.logout_user()
        return redirect(url_for('.index'))