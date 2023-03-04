from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"

db = SQLAlchemy()
migrate = Migrate()

from flask_admin import Admin
from osemu.admin.index import LoginAdminIndexView
admin = Admin(name='OSEmu', template_mode='bootstrap4', index_view=LoginAdminIndexView(), base_template='admin_master.html')
