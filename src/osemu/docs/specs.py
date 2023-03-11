#APISpec
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

spec = APISpec(
    title="Open-source Emulator Database",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Marshmallow schemas
from osemu.api import schema
spec.components.schema("Languages", schema=schema.LanguageSchema)
spec.components.schema("Company", schema=schema.CompanySchema)
spec.components.schema("Console", schema=schema.ConsoleSchema)
spec.components.schema("Emulator", schema=schema.EmulatorSchema)
spec.components.schema("User", schema=schema.UserSchema)

# Flask login authentication
api_key_scheme = {"type": "apiKey", "in": "cookie", "name": "remember_token"}
spec.components.security_scheme("cookieAuth", api_key_scheme)

# API views
def register_views_on_spec():

    # Authentication
    from osemu.api.views import auth
    spec.path(view=auth.get_user)
    spec.path(view=auth.signup)
    spec.path(view=auth.login)
    spec.path(view=auth.logout)

    # Emulators
    from osemu.api.views import emulators
    spec.path(view=emulators.emulator_entry_view)
    spec.path(view=emulators.emulator_group_view)

    # Consoles
    from osemu.api.views import consoles
    spec.path(view=consoles.console_entry_view)
    spec.path(view=consoles.console_group_view)
    spec.path(view=consoles.emulators_for_console_view)

    # Company
    from osemu.api.views import companies
    spec.path(view=companies.company_entry_view)
    spec.path(view=companies.company_group_view)

    # Languages
    from osemu.api.views import languages
    spec.path(view=languages.language_entry_view)
    spec.path(view=languages.language_group_view)

    # Licenses
    from osemu.api.views import licenses
    spec.path(view=licenses.license_entry_view)
    spec.path(view=licenses.license_group_view)
