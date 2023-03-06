import os
from flask import Flask, jsonify
from .extensions import db, migrate, login_manager, admin
from .api.models import *
from .config import DevelopmentConfig
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

def create_app(config=DevelopmentConfig, init_db=True):

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    from osemu.admin.views import register_admin_views
    register_admin_views()

    from .api import api_bp
    app.register_blueprint(api_bp)

    from osemu.api.views.docs import swaggerui_bp
    app.register_blueprint(swaggerui_bp)

    from osemu.docs.specs import register_views_on_spec
    with app.app_context():
        register_views_on_spec()
    
    return app

