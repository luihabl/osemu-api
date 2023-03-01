from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin

login_manager = LoginManager()
login_manager.session_protection = "strong"

db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='OSEmu', template_mode='bootstrap3')
