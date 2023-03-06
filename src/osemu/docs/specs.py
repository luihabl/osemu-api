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

from osemu.api import schema
spec.components.schema("Company", schema=schema.CompanySchema)
spec.components.schema("Console", schema=schema.ConsoleSchema)
spec.components.schema("Languages", schema=schema.LanguageSchema)
spec.components.schema("Emulator", schema=schema.EmulatorSchema)
spec.components.schema("User", schema=schema.UserSchema)

