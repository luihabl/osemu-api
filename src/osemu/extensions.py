# Flask-Login
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"

# Flask-Sqlalchemy and Flask-Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# Flask-Admin
from flask_admin import Admin
from osemu.admin.index import LoginAdminIndexView
admin = Admin(name='OSEmu', template_mode='bootstrap4', index_view=LoginAdminIndexView(), base_template='admin_master.html')

# Flask-APScheduler
from flask_apscheduler import APScheduler
scheduler = APScheduler()
